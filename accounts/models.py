from django.db import models
from django.contrib.auth.models import User


class BlogUser(User):
    profile_description = models.TextField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    followed_users = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
