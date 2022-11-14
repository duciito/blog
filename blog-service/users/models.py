from django.db import models
from django.contrib.auth.models import AbstractUser


class BlogUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_description = models.TextField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    followed_users = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    saved_articles = models.ManyToManyField(
        'core.Article',
        related_name='users_saved',
        blank=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def total_articles(self):
        from core.models import Article
        return Article.objects.filter(creator=self).count()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
