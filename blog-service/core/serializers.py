from django.db import IntegrityError, transaction
from rest_framework import serializers

from core.models import Article, ArticleContent, Category, Comment, EditableModel
from users.serializers import UserSerializer
from common.serializers import FollowableModelSerializer


class EditableModelSerializer(serializers.ModelSerializer):
    """Base serializer for comments and posts."""
    total_votes = serializers.ReadOnlyField()
    voted = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.query_params.get('nested'):
            self.fields['creator'] = UserSerializer(read_only=True,
                    context={'request': request})

    def get_voted(self, obj):
        user = self.context['request'].user
        # TODO: May not be the safest way to go about this
        return type(obj).objects.filter(id=obj.id, voters=user).exists()


class CategorySerializer(FollowableModelSerializer):
    """Category serializer"""

    class Meta:
        model = Category
        exclude = ('followers',)

    def create(self, validated_data):
        # Allow passing nested articles with category creation.
        articles = validated_data.pop('articles', None)
        category = super().create(validated_data)

        if articles:
            Article.objects.bulk_create([
                Article(**article_data) for article_data in articles
            ])

        return category


class ArticleContentSerializer(serializers.ModelSerializer):
    """Article content serializer. Can come nested with article data."""

    class Meta:
        model = ArticleContent
        fields = '__all__'
        read_only_fields = ('guid',)


class CommentSerializer(EditableModelSerializer):
    """Comment serializer. You can only comment on articles."""

    class Meta:
            model = Comment
            exclude = ('voters',)

    
class LightArticleSerializer(EditableModelSerializer):
    """Article serializer used for serializing only the essentials."""
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('voters', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.query_params.get('nested'):
            self.fields['category'] = CategorySerializer(read_only=True)

    def get_saved(self, obj):
        user = self.context['request'].user
        return Article.objects.filter(id=obj.id, users_saved=user).exists()


class ArticleSerializer(LightArticleSerializer):
    """Article serializer. Serializes text and computes votes number."""

    article_content_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta(LightArticleSerializer.Meta):
        exclude = ('voters',)
        read_only_fields = ('creator',)

    def create(self, validated_data):
        # Pop contents before saving to avoid unknown field error.
        article_contents = validated_data.pop('article_content_ids', [])

        try:
            # Either all contents save along with the article,
            # or nothing is saved at all.
            with transaction.atomic():
                article = Article.objects.create(**validated_data)
                # Bulk update all article contents to point to the right article.
                ArticleContent.objects.filter(id__in=article_contents).update(
                    article=article
                )
        except IntegrityError:
            raise serializers.ValidationError('Article couldn\'t save. Please \
                    check you\'re attaching valid media.')

        return article
