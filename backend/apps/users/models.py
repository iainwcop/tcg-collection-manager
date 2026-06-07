from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Application user. Extend as profile fields are needed."""

    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email or self.username
