from rest_framework.decorators import action
from rest_framework import response, status


class VotableContentMixin:
    """
    A mixin that allows people to like/unlike content.
    The model in question should be associated with `BlogUser`
    and the related queryset name should be named 'voters'.
    """
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        """Increment votes for an object."""
        obj = self.get_object()
        obj.voters.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unvote(self, request, pk=None):
        """
        Remove vote for an object.
        Doesn't thrown an exception if the user hasn't voted.
        """
        obj = self.get_object()
        obj.voters.remove(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FollowableContentMixin:
    """
    A mixin that allows people to follow/unfollow users/categories.
    The related name is expected to be `followers`.
    """
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow an object."""
        obj = self.get_object()
        obj.followers.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow an object."""
        obj = self.get_object()
        obj.followers.remove(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get all followers for an obj."""
        obj = self.get_object()
        serializer = self.get_serializer_class()
        followers = serializer(obj.followers, many=True)
        return response.Response(followers.data)
