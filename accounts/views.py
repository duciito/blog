from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate, logout
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import (
    LoginSerializer, SignupSerializer, AuthUserSerializer
)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_classes = {
        'login': LoginSerializer,
        'signup': SignupSerializer
    }

    @action(methods=['POST'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self._get_and_auth_user(**serializer.validated_data)
        success_data = AuthUserSerializer(user).data
        return Response(data=success_data)

    @action(methods=['POST'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        success_data = AuthUserSerializer(user).data
        return Response(data=success_data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(data={'success': 'Logged out successfully!'})

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict.')

        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def _get_and_auth_user(username, password):
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username/password.")

        return user
