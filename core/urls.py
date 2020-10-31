# core/urls.py
from rest_framework import routers
from core.views import CategoriesViewSet, ArticlesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('articles', ArticlesViewSet, basename='articles')

urlpatterns = router.urls
