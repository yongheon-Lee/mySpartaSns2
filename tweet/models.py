from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager


# Create your models here.
class Tweet(models.Model):
    class Meta:
        db_table = 'tweet'

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시, 현재 시간 자동 추가
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시, 현재 시간 자동 저장


class TweetComment(models.Model):
    class Meta:
        db_table = 'comment'

    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
