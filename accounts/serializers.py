from rest_framework.authtoken.models import Token
from rest_framework import serializers, validators

from accounts.models import BlogUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    """Base user serializer."""

    class Meta:
        model = BlogUser
        fields = ('id',
                'username',
                'first_name',
                'last_name',
                'is_active',
                'email',
                'profile_description',
                'joined_at',
                'followed_users')
        read_only_fields = ('is_active', 'joined_at', )


class LoginSerializer(serializers.Serializer):
    """Login credentials serializer."""

    email = serializers.CharField(
        max_length=300,
        required=True,
    )
    password = serializers.CharField(required=True, write_only=True)


class SignupSerializer(serializers.ModelSerializer):
    """Signup user data serializer."""

    class Meta:
        model = BlogUser
        fields = ('username', 'email',
                'password', 'first_name',
                'last_name', 'profile_description')

    def validate_email(self, value):
        """Check to see if taken."""

        # `filter` instead of `get` to not get an exception.
        user = BlogUser.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email already taken!")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        """Validate password according to validators declared in settings."""

        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return BlogUser.objects.create_user(**validated_data)


class AuthUserSerializer(UserSerializer):
    """Used to serialize data of successfully authenticated users."""

    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('auth_token',)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        # Request is passed with context by default
        # with recent versions of Django.
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match!')

        return value

    def validate_new_password(self, value):
        """Validate password similar to how it's validated when signing up."""

        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        # Update password through serializer save.
        user = self.context['request'].user
        user.set_password(validated_data['new_password'])
