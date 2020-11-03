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
        article = self.get_object()
        article.voters.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unvote(self, request, pk=None):
        article = self.get_object()
        article.voters.remove(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def hot(self, request):
        pass


class ArticleContentsViewSet(viewsets.ModelViewSet):
    queryset = ArticleContent.objects.all()
    serializer_class = ArticleContentSerializer
