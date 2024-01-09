# core/urls.py
from django.conf.urls import url
from rest_framework import routers

from core.views import (
    ArticleContentsViewSet,
    ArticlesViewSet,
    CategoriesViewSet,
    CommentsView,
    SearchView,
)

app_name = "core"

router = routers.DefaultRouter()
router.register("categories", CategoriesViewSet, basename="categories")
router.register("articles", ArticlesViewSet, basename="articles")
router.register(
    "article_contents", ArticleContentsViewSet, basename="articles-contents"
)
router.register("comments", CommentsView, basename="comments")

urlpatterns = router.urls
urlpatterns.extend([url("search", SearchView.as_view())])
