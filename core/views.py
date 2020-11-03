from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import response, viewsets, status
from rest_framework.decorators import action

from core.serializers import (
    CategorySerializer, ArticleSerializer, ArticleContentSerializer
)
from core.models import Category, Article, ArticleContent


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False)
    def articles(self, request):
        pass


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        request.data.setdefault('creator', request.user.pk)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        """Vote for an article."""
        article = self.get_object()
        article.voters.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unvote(self, request, pk=None):
        """
        Remove vote for an article.
        Doesn't thrown an exception if the user hasn't voted.
        """
        article = self.get_object()
        article.voters.remove(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def hot(self, request):
        """Get articles that have gained popularity quickly."""
        last_three_days = timezone.now() - timedelta(days=3)
        serializer = self.get_serializer_class()
        queryset = self.get_queryset()

        queryset = queryset.annotate(
            num_voters=Count('voters'),
            num_comments=Count('comments')
        ).filter(
            num_voters__gte=5,
            num_comments__gt=2,
            posted_at__gte=last_three_days
        )

        # Serialize new queryset using view's serializer.
        result = serializer(queryset, many=True)
        return response.Response(result.data)


class ArticleContentsViewSet(viewsets.ModelViewSet):
    queryset = ArticleContent.objects.all()
    serializer_class = ArticleContentSerializer
