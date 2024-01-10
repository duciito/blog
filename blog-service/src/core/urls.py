# core/urls.py
from core.views import (
    ArticleContentsViewSet,
    ArticlesViewSet,
    CategoriesViewSet,
    CommentsView,
    SearchView,
)
from django.urls import path
from rest_framework import routers

app_name = "core"

router = routers.DefaultRouter()
router.register("categories", CategoriesViewSet, basename="categories")
router.register("articles", ArticlesViewSet, basename="articles")
router.register(
    "article_contents", ArticleContentsViewSet, basename="articles-contents"
)
router.register("comments", CommentsView, basename="comments")

urlpatterns = router.urls
urlpatterns.extend([path("search", SearchView.as_view(), name="search")])
