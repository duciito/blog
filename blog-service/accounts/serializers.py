from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers, validators
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from pytz import utc

from accounts.models import BlogUser
from common.serializers import FollowableModelSerializer


class UserSerializer(FollowableModelSerializer):
    """Base user serializer."""

    def __init__(self, *args, **kwargs):
        # Add unnecessary stuff only if needed.
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request:
            extra_info = request.query_params.get('extra_info')
            if extra_info:
                self.fields['total_articles'] = serializers.ReadOnlyField();
                self.Meta.fields.extend([
                    'followed_users',
                    'total_articles'
                ])

    class Meta:
        model = BlogUser
        fields = ['id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_active',
                  'email',
                  'profile_description',
                  'joined_at',
                  'followed',
                  'total_followers']
        read_only_fields = ('is_active', 'joined_at', )
