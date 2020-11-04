# core/urls.py
from rest_framework import routers
from core.views import (
    CategoriesViewSet, ArticlesViewSet, ArticleContentsViewSet
)

app_name = 'core'

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('articles', ArticlesViewSet, basename='articles')
router.register('articles_contents', ArticleContentsViewSet, basename='articles-contents')

urlpatterns = router.urls
