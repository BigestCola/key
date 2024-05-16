# cdkey/models.py

from django.db import models
from user.models import CDKey 
from .constants import DURATION_CHOICES
from user.models import User



class CDKeyExtractRecord(models.Model):
    cdkey = models.ForeignKey(CDKey, on_delete=models.CASCADE, related_name='extract_records')
    device_id = models.CharField(max_length=255)
    app_version = models.CharField(max_length=255)
    extract_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cdkey_extract_record'

