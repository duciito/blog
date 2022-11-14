from rest_framework import serializers

from users.models import BlogUser
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
