from django.db import IntegrityError, transaction
from rest_framework import serializers

from core.models import Article, ArticleContent, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer that also lists related articles."""

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


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer. You can only comment on articles."""

    total_votes = serializers.ReadOnlyField()

    def __init__(self, *args, **kwargs):
        # Remove article id if used for nested data.
        nested = kwargs.pop('nested', None)
        super().__init__(*args, **kwargs)

        if nested:
            self.fields.pop('article')

    class Meta:
        model = Comment
        exclude = ('voters',)


class LightArticleSerializer(serializers.ModelSerializer):
    """Article serializer used for serializing only the essentials."""
    total_votes = serializers.ReadOnlyField()
    voted = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ('voters', 'text')

    def get_voted(self, obj):
        user = self.context['request'].user
        return Article.objects.filter(id=obj.id, voters=user).exists()

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
