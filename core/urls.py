# core/urls.py
from rest_framework import routers
from core.views import (
    CategoriesViewSet, ArticlesViewSet, ArticleContentsViewSet,
    CommentsCreateView
)
from django.conf.urls import url

app_name = 'core'

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')
router.register('articles', ArticlesViewSet, basename='articles')
router.register('article_contents', ArticleContentsViewSet, basename='articles-contents')

urlpatterns = router.urls
urlpatterns.extend([
    url('comments', CommentsCreateView.as_view())
])
