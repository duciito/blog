import logging
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate
from django.db.models import Count
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import (
    AuthUserSerializer, LoginSerializer,
    PasswordChangeSerializer, SignupSerializer,
    UserSerializer
)
from accounts.models import BlogUser
from services.aws_utils import ses_verify_email_address

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.GenericViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)
    serializer_classes = {
        'login': LoginSerializer,
        'signup': SignupSerializer,
        'password_change': PasswordChangeSerializer
    }

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
        success_data = AuthUserSerializer(user).data
        try:
            ses_verify_email_address(user.email)
        except:
            logger.warning(f'Could not verify {user}\'s email for SES handling.')

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
        email = request.POST.get('email')
        user_exists = BlogUser.objects.filter(email=email).exists()

        if user_exists:
            pass

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict.')

        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def _get_and_auth_user(self, email, password):
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username/password.")

        return user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = BlogUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset

        followers_only = self.request.query_params.get('followers_only')
        if followers_only:
            queryset = queryset.filter(
                followed_users=self.request.user
            )

        return queryset

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow an user."""
        user = self.get_object()
        user.followers.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
