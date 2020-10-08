import uuid

from django.db import models
from django.conf import settings
from accounts.models import BlogUser


class EditableModel(models.Model):
    creator = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True, null=True)
    # This one triggers differently.
    # It updated the field on each save.
    edited_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=200)


class Article(EditableModel):
    category = models.ForeignKey(
        Category,
        related_name='articles',
        null=True,
        on_delete=models.SET_NULL
    )
    voters = models.ManyToManyField(BlogUser, related_name='liked_articles', blank=True)
    title = models.CharField(max_length=255)
    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        default=f'{settings.SITE_URL}{settings.STATIC_URL}images/default-article.png'
    )


class ArticleContent(models.Model):
    # Content type choices.
    # The second attr provides readable name in django forms.
    CONTENT_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    article = models.ForeignKey(Article, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    url = models.URLField(max_length=500)
    guid = models.UUIDField(null=True, default=uuid.uuid4, unique=True)
    order_index = models.PositiveIntegerField()


class Comment(EditableModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    voters = models.ManyToManyField(BlogUser, related_name='liked_comments', blank=True)
