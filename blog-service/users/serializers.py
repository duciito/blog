from rest_framework import serializers

from common.serializers import FollowableModelSerializer
from users.models import BlogUser


class UserSerializer(FollowableModelSerializer):
    """Base user serializer."""

    def __init__(self, *args, **kwargs):
        # Add unnecessary stuff only if needed.
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request:
            extra_info = request.query_params.get("extra_info")
            if extra_info:
                self.fields["total_articles"] = serializers.ReadOnlyField()
                self.Meta.fields.extend(["followed_users", "total_articles"])

    class Meta:
        model = BlogUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_description",
            "joined_at",
            "followed",
            "total_followers",
        ]
