from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import response, viewsets, status, generics
from rest_framework.decorators import action

from core.serializers import (
    ArticleContentSerializer, ArticleSerializer,
    CategorySerializer, CommentSerializer,
    LightArticleSerializer
)
from core.models import Article, ArticleContent, Category, Comment
from core.mixins import VotableContentMixin
from core.search import filter_articles, filter_categories, filter_users
from accounts.serializers import UserSerializer
from accounts.models import BlogUser


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False)
    def articles(self, request):
        pass

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Start following a category."""
        category = self.get_object()
        category.followers.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get all followers for a category."""
        category = self.get_object()
        followers = UserSerializer(category.followers, many=True)
        return response.Response(followers.data)

class ArticlesViewSet(VotableContentMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # Actions that require only essential data.
    light_actions = ('list', 'hot', 'retrieve')

    def get_queryset(self):
        queryset = self.queryset

        category = self.request.query_params.get('category_id')
        if category:
            queryset = queryset.filter(
                category=category
            )

        return queryset

    def get_serializer_class(self):
        # Avoid serializing heavy data in list get unless specified otherwise.
        full_data = self.request.query_params.get('full_data')
        if full_data or self.action not in self.light_actions:
            return ArticleSerializer

        return LightArticleSerializer

    def perform_create(self, serializer):
        # Creator should be only the user the request is coming from.
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['get'])
    def text(self, request, pk=None):
        """Get the text content of an article. Could be raw HTML."""
        article = self.get_object()
        return response.Response(article.text)

    @action(detail=True, methods=['post'])
    def save(self, request, pk=None):
        """Save an article."""
        article = self.get_object()
        article.users_saved.add(request.user)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def unsave(self, request, pk=None):
        """Remove article from saved."""
        article = self.get_object()
        article.users_saved.remove(request.user)
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

    def list(self, request, *args, **kwargs):
        article = self.request.query_params.get('article_id', None)
        queryset = None

        if article:
            queryset = self.filter_queryset(self.queryset.filter(article=article))

        if queryset is None:
            return response.Response(
                data="You need to pass `article_id` when getting the article contents",
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class CommentsView(VotableContentMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = self.queryset

        article = self.request.query_params.get('article_id')
        if article:
            queryset = queryset.filter(article=article)

        return queryset


class SearchView(generics.ListAPIView):
    serializer_classes = {
        'article': ArticleSerializer,
        'category': CategorySerializer,
        'user': UserSerializer
    }

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        search_expression = self.request.query_params.get('search_expression')
        queryset = None

        if content_type and search_expression:
            if content_type == 'article':
                queryset = filter_articles(
                    Article.objects.all(),
                    search_expression
                )
            elif content_type == 'category':
                queryset = filter_categories(
                    Category.objects.all(),
                    search_expression
                )
            elif content_type == 'user':
                queryset = filter_users(
                    BlogUser.objects.all(),
                    search_expression
                )

        return queryset

    def get_serializer_class(self):
        content_type = self.request.query_params.get('content_type')

        if content_type in self.serializer_classes:
            return self.serializer_classes[content_type]

        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """Dynamically return a filtered queryset depending on the content type passed."""
        queryset = self.filter_queryset(self.get_queryset())
        if queryset is None:
            return response.Response(
                data="Wrong parameters provided. You need to pass valid `content_type` and `search_expression`",
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

