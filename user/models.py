from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser):
    class Meta:
        db_table = 'user'

    bio = models.TextField(max_length=500, blank=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
