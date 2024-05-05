# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, '管理员'),
        (2, '一级代理'),
        (3, '二级代理'),
    )

    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('agent', '代理'),
    )

    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='agent')
    user_type = models.SmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    is_active = models.BooleanField(default=True)
    monthly_quota = models.IntegerField(default=0)
    day_quota = models.IntegerField(default=0)
    quota_updated_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user'

