# cdkey/models.py

from django.db import models
from user.models import User
from .constants import DURATION_CHOICES

class CDKey(models.Model):
    expire_time = models.DateTimeField()
    STATUS_CHOICES = (
        (1, '未使用'),
        (2, '已使用'),
        (3, '已过期'),
    )

    cdkey = models.CharField(max_length=64, unique=True)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cdkeys')
    extract_time = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'cdkey'

