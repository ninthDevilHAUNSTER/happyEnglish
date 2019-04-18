from django.db import models
from django.contrib.auth.models import AbstractUser
# from datetime import datetime
import django.utils.timezone as timezone


class UserProfile(AbstractUser):
    '''
    common user
    之后会逐渐加入模型
    '''
    nickname = models.CharField(max_length=50, default="无名大侠", verbose_name="昵称")

    # create_time = models.DateTimeField(default=timezone.now, verbose_name="创建日期")

    def __str__(self):
        return self.username

# Create your models here.
