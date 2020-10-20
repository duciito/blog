from rest_framework import serializers
from core.models import Category, Article


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer that also lists related aritcles."""

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
