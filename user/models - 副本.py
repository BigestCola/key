# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class CDKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_cdkeys')

    def __str__(self):
        return self.key

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    remaining_quota = models.PositiveIntegerField(default=0)
    total_quota = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def increase_quota(self, amount):
        self.remaining_quota += amount
        self.total_quota += amount
        self.save()

    def decrease_quota(self, amount):
        if self.remaining_quota >= amount:
            self.remaining_quota -= amount
            self.save()
            return True
        return False

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

