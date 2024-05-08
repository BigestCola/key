# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

class CDKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_cdkeys')
    used_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='used_cdkeys', null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    validity_days = models.IntegerField(choices=[(1, '1 天'), (31, '31 天')], default=1)

    def is_expired(self):
        return self.expires_at < timezone.now()

    def is_used(self):
        return self.used_by is not None

    def mark_as_used(self, user):
        if not self.is_used() and not self.is_expired():
            self.used_by = user
            self.used_at = timezone.now()
            self.save()
            return True
        return False

    def __str__(self):
        return self.key

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

    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates', verbose_name='上级')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='agent', verbose_name='角色')
    user_type = models.SmallIntegerField(choices=USER_TYPE_CHOICES, default=3, verbose_name='用户类型')
    is_active = models.BooleanField(default=True,verbose_name='是否激活')
    monthly_quota = models.IntegerField(default=0,verbose_name='月度配额')
    day_quota = models.IntegerField(default=0, verbose_name='日配额')
    quota_updated_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user'

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    credit = models.IntegerField(default=0)
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
    return user.user_type == 1

def is_first_level_agent(user):
    return user.user_type == 2

def is_second_level_agent(user):
    return user.user_type == 3

def can_manage_user(request_user, managed_user):
    if is_admin(request_user):
        return True
    elif is_first_level_agent(request_user) and is_second_level_agent(managed_user):
        return managed_user.superior == request_user
    else:
        return False