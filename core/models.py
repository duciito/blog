import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.conf import settings

from core.utils import file_cleanup
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
    followers = models.ManyToManyField(
        BlogUser,
        related_name='followed_categories',
        blank=True
    )

    @property
    def total_followers(self):
        return self.followers.count()

    def __str__(self):
        return self.name


class Article(EditableModel):
    category = models.ForeignKey(
        Category,
        related_name='articles',
        null=True,
        on_delete=models.SET_NULL
    )
    voters = models.ManyToManyField(BlogUser, related_name='liked_articles', blank=True)
    title = models.CharField(max_length=255)
    thumbnail = models.FileField(blank=True)

    @property
    def total_votes(self):
        return self.voters.count()

    def __str__(self):
        return f"{self.title} by {self.creator}"


class ArticleContent(models.Model):
    # Content type choices.
    # The second attr provides readable name in django forms.
    CONTENT_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    article = models.ForeignKey(Article, null=True, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    file = models.FileField()
    guid = models.UUIDField(null=True, default=uuid.uuid4, unique=True)


class Comment(EditableModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    voters = models.ManyToManyField(BlogUser, related_name='liked_comments', blank=True)

    @property
    def total_votes(self):
        return self.voters.count()


# Signals
pre_delete.connect(file_cleanup, sender=Article)
pre_delete.connect(file_cleanup, sender=ArticleContent)
