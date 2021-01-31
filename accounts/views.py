import logging
from functools import partial

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import DjangoUnicodeDecodeError, smart_bytes, smart_str
from django.urls import reverse
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import (
    AuthUserSerializer, LoginSerializer,
    PasswordChangeSerializer, SignupSerializer,
    UserSerializer, PasswordResetSerializer
)
from accounts.models import BlogUser
from accounts.utils import build_url
from config import settings
from services.aws_utils import ses_verify_email_address
from core.serializers import LightArticleSerializer

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.GenericViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)
    serializer_classes = {
        'login': LoginSerializer,
        'signup': SignupSerializer,
        'password_change': PasswordChangeSerializer,
        'password_reset_data': PasswordResetSerializer
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict.')

        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self._get_and_auth_user(**serializer.validated_data)
        success_data = AuthUserSerializer(user).data
        return Response(data=success_data)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        try:
            ses_verify_email_address(user.email)
        except:
            logger.warning(f'Could not verify {user}\'s email for SES handling.')

        success_data = AuthUserSerializer(user).data
        return Response(data=success_data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        # Delete the token to force a login.
        request.user.auth_token.delete()
        return Response(data={'success': 'Logged out successfully!'})

    @action(methods=['POST'], permission_classes=[IsAuthenticated], detail=False)
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def password_reset(self, request):
        email = request.data.get('email')
        user_query = BlogUser.objects.filter(email=email)

        if user_query.exists():
            user = user_query.get()
            # Safely encode user id in base64
            user_id_base64 = urlsafe_base64_encode(smart_bytes(user.id))
            # Generate a one-time token that expires in 24h.
            token = PasswordResetTokenGenerator().make_token(user)
            # Get a redirect url for when it's a valid token.
            redirect_url = request.data.get('redirect_url', '')
            # Get the confirm url.
            absolute_url = self._build_password_reset_url(
                user_id_base64,
                token,
                redirect_url
            )
            # Send the actual email.
            send_mail(
                subject='Reset your password',
                message=f'Click the link below to reset password.\n{absolute_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False, url_name='password-verify')
    def password_reset_verify(self, request):
        uidb64 = request.query_params.get('uidb64')
        token = request.query_params.get('token')
        redirect_url = request.query_params.get('redirect_url')
        # Saves some typing to bind some repetitive arguments
        redirect_url_with_params = partial(
            build_url,
            url=redirect_url
        )

        try:
            # Decode information back
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = BlogUser.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return redirect(redirect_url_with_params(
                    get_params={
                        'token_valid': False,
                        'reason': 'Token has expired!'
                    }
                ))

            # If it's valid, pass the uid and token one more time,
            # since we're gonna need them (when a new password is finally
            # submitted) to once again make sure the token has not expired.
            return redirect(redirect_url_with_params(
                get_params={
                    'token_valid': True,
                    'uidb64': uidb64,
                    'token': token
                }
            ))

        except (AttributeError, TypeError, ValueError, DjangoUnicodeDecodeError) as e:
            return redirect(redirect_url_with_params(
                get_params={
                    'token_valid': False,
                    'reason': 'Token or user id is invalid.'
                }
            ))

    @action(methods=['POST'], detail=False)
    def password_reset_data(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_and_auth_user(self, email, password):
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username/password.")

        return user

    def _build_password_reset_url(self, uid, token, redirect_url):
        current_site = get_current_site(self.request).domain
        # Build custom url with uid and token get params.
        confirm_link = build_url(
            'accounts:auth-password-verify',
            get_params={
                'uidb64': uid,
                'token': token,
                'redirect_url': redirect_url
            }
        )
        return f'http://{current_site}{confirm_link}'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow a user."""
        user = self.get_object()
        user.followers.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow a user."""
        user = self.get_object()
        user.followers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get all followers for a user."""
        user = self.get_object()
        serializer = self.get_serializer_class()
        followers = serializer(user.followers, many=True)
        return Response(followers.data)

    @action(detail=True, methods=['get'])
    def saved_articles(self, request, pk=None):
        """Get all saved articles for the logged in user."""
        if request.user.id == int(pk):
            user = self.get_object()
            saved_articles = LightArticleSerializer(
                user.saved_articles,
                many=True,
                context={'request': request}
            )
            return Response(saved_articles.data)
        # Can't access other users' saved articles.
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular users that have gained a number of followers."""
        serializer = self.get_serializer_class()
        queryset = self.get_queryset()

        queryset = queryset.annotate(
            num_followers=Count('followers'),
        ).filter(
            num_followers__gte=5,
        )

        # Serialize new queryset using view's serializer.
        result = serializer(queryset, many=True)
        return Response(result.data)
