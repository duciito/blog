from rest_framework import serializers


class FollowableModelSerializer(serializers.ModelSerializer):
    total_followers = serializers.ReadOnlyField()
    followed = serializers.SerializerMethodField()

    def get_followed(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            return type(obj).objects.filter(id=obj.id, followers=user).exists()

        return None
