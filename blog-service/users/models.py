from django.db import models


class BlogUser(models.Model):
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

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def total_articles(self):
        from core.models import Article
        return Article.objects.filter(creator=self).count()
