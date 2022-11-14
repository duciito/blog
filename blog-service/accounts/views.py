import logging

from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from accounts.models import BlogUser
from core.serializers import LightArticleSerializer
from core.mixins import FollowableContentMixin
from core.pagination import StandardResultsSetPagination

logger = logging.getLogger(__name__)


class UsersViewSet(viewsets.ModelViewSet, FollowableContentMixin):
    queryset = BlogUser.objects.all()
    serializer_class = UserSerializer
    pagination_class =  StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def followed_users(self, request, pk=None):
        """Get all followed users for a user."""
        user = self.get_object()
        serializer = self.get_serializer_class()
        followed_users = serializer(user.followed_users,
                many=True,
                context={'request': request})
        return Response(followed_users.data)

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
        result = serializer(queryset,
                many=True,
                context={'request': request})
        return Response(result.data)
