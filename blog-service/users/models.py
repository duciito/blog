from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(models.Manager):
    def create_from_event(self, data: dict):
        # WARNING: for now fields are called exactly the same
        # as in the User model, so we might have to manually
        # map them if they ever change names.
        return self.create(**data)


class BlogUser(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
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

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def total_articles(self):
        from core.models import Article
        return Article.objects.filter(creator=self).count()

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
