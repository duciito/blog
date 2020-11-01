from rest_framework import viewsets
from rest_framework.decorators import action

from core.serializers import CategorySerializer, ArticleSerializer
from core.models import Category, Article


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
