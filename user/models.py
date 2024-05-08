# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

def is_admin(user):
    return user.user_type == 'ADMIN'

def is_first_level_agent(user):
    return user.user_type == 'FIRST_LEVEL_AGENT'

def is_second_level_agent(user):
    return user.user_type == 'SECOND_LEVEL_AGENT'

def can_manage_user(request_user, managed_user):
    if is_admin(request_user):
        return True
    elif is_first_level_agent(request_user) and is_second_level_agent(managed_user):
        return managed_user.superior == request_user
    else:
        return False

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

