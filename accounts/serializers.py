from rest_framework.authtoken.models import Token
from rest_framework import serializers, validators

from accounts.models import BlogUser


class UserSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(
        max_length=300,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=BlogUser.objects.all(),
                message='A user with this email address already exists.',
            )
        ]
    )
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(UserSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, user):
        token = Token.objects.get_or_create(user=user)
        return token.key

