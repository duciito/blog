from rest_framework import serializers
from core.models import Category, Article, ArticleContent


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer that also lists related articles."""

    class Meta:
        model = Category
        fields = '__all__'

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


class ArticleSerializer(serializers.ModelSerializer):
    """Article serializer. Serializes text and computes votes number."""
    total_votes = serializers.ReadOnlyField()
    article_contents = ArticleContentSerializer(many=True, required=False)

    class Meta:
        model = Article
        exclude = ('voters',)

    def create(self, validated_data):
        # Pop contents before saving to avoid unknown field error.
        article_contents = validated_data.pop('article_contents')
        article = Article.objects.create(**validated_data)

        ArticleContent.objects.bulk_create([
            ArticleContent(**data) for data in article_contents
        ])

        return article
