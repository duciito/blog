from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, response, status, viewsets
from rest_framework.decorators import action
from users.models import BlogUser
from users.serializers import UserSerializer

from core.mixins import FollowableContentMixin, VotableContentMixin
from core.models import Article, ArticleContent, Category, Comment
from core.pagination import StandardResultsSetPagination
from core.search import filter_articles, filter_categories, filter_users
from core.serializers import (
    ArticleContentSerializer,
    ArticleSerializer,
    CategorySerializer,
    CommentSerializer,
    LightArticleSerializer,
)


class CategoriesViewSet(viewsets.ModelViewSet, FollowableContentMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticlesViewSet(VotableContentMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # Actions that require only essential data.
    light_actions = ("list", "hot", "retrieve")
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        category_id = self.request.query_params.get("category_id")
        desc_order = self.request.query_params.get("desc_order")

        if user_id:
            queryset = queryset.filter(creator=user_id)

        if category_id:
            queryset = queryset.filter(category=category_id)

        if desc_order:
            queryset = queryset.order_by("-posted_at")

        return queryset

    def get_serializer_class(self):
        # Avoid serializing heavy data in list get unless specified otherwise.
        full_data = self.request.query_params.get("full_data")
        if full_data or self.action not in self.light_actions:
            return ArticleSerializer

        return LightArticleSerializer

    def perform_create(self, serializer):
        # Creator should be only the user the request is coming from.
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["get"])
    def text(self, request, pk=None):
        """Get the text content of an article. Could be raw HTML."""
        article = self.get_object()
        return response.Response(article.text)

    @action(detail=True, methods=["post"])
    def save(self, request, pk=None):
        """Save an article."""
        article = self.get_object()
        article.users_saved.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def unsave(self, request, pk=None):
        """Remove article from saved."""
        article = self.get_object()
        article.users_saved.remove(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def hot(self, request):
        """Get articles that have gained popularity quickly."""
        # last_month = timezone.now() - timedelta(days=30)
        queryset = self.get_queryset()

        queryset = (
            queryset.annotate(
                num_voters=Count("voters"), num_comments=Count("comments")
            )
            .filter(
                num_voters__gte=1,
                num_comments__gt=0,
                # posted_at__gte=last_month
            )
            .order_by("-num_voters")
        )

        return self._paginate_custom_action(queryset)

    @action(detail=False, methods=["get"])
    def recent_from_following(self, request):
        """Get recent articles from your subscriptions."""
        last_seven_days = timezone.now() - timedelta(days=7)
        followed_users = request.user.followed_users.all()
        queryset = self.get_queryset()

        queryset = queryset.filter(
            creator__in=followed_users, posted_at__gte=last_seven_days
        )

        return self._paginate_custom_action(queryset)

    def _paginate_custom_action(self, queryset):
        # Paginate and serialize new queryset using view's serializer.
        page = self.paginate_queryset(queryset)
        result = self.get_serializer(page, many=True, context={"request": self.request})
        return self.get_paginated_response(result.data)


class ArticleContentsViewSet(viewsets.ModelViewSet):
    queryset = ArticleContent.objects.all()
    serializer_class = ArticleContentSerializer

    def list(self, request, *args, **kwargs):
        article = self.request.query_params.get("article_id", None)
        queryset = None

        if article:
            queryset = self.filter_queryset(self.queryset.filter(article=article))

        if queryset is None:
            return response.Response(
                data="You need to pass `article_id` when getting the article contents",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class CommentsView(VotableContentMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset

        article = self.request.query_params.get("article_id")
        if article:
            queryset = queryset.filter(article=article)

        newest_first = self.request.query_params.get("newest_first")
        if newest_first:
            queryset = queryset.order_by("-posted_at")

        return queryset


class SearchView(generics.ListAPIView):
    serializer_classes = {
        "article": ArticleSerializer,
        "category": CategorySerializer,
        "user": UserSerializer,
    }

    def get_queryset(self):
        content_type = self.request.query_params.get("content_type")
        search_expression = self.request.query_params.get("search_expression")
        queryset = None

        if content_type and search_expression:
            if content_type == "article":
                queryset = filter_articles(Article.objects.all(), search_expression)
            elif content_type == "category":
                queryset = filter_categories(Category.objects.all(), search_expression)
            elif content_type == "user":
                queryset = filter_users(BlogUser.objects.all(), search_expression)

        return queryset

    def get_serializer_class(self):
        content_type = self.request.query_params.get("content_type")

        if content_type in self.serializer_classes:
            return self.serializer_classes[content_type]

        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """
        Dynamically return a filtered queryset depending on the content type passed.
        """
        queryset = self.filter_queryset(self.get_queryset())
        if queryset is None:
            return response.Response(
                data=(
                    "Wrong parameters provided. You need to pass "
                    "valid `content_type` and `search_expression`"
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
