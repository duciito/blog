import uuid

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class BlogUser(User):
    profile_description = models.TextField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    followed_users = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )


class Category(models.Model):
    name = models.CharField(max_length=200)


class Article(models.Model):
    creator = models.ForeignKey(
        BlogUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    category = models.ForeignKey(Category, related_name='articles')
    voters = models.ManyToManyField(BlogUser, related_name='voted_articles', blank=True)
    title = models.CharField(max_length=255)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)
    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
        default=f'{settings.SITE_URL}{settings.STATIC_URL}images/default-article.png'
    )
    text = models.TextField()


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
