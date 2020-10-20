from rest_framework import viewsets
from rest_framework.decorators import action

from core.serializers import CategorySerializer
from core.models import Category


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False)
    def articles(self, request):
        pass
