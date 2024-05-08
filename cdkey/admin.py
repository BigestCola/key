# cdkey/admin.py

from django.contrib import admin
from .models import CDKey

@admin.register(CDKey)
class CDKeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'cdkey', 'status', 'user', 'create_time', 'extract_time']
    search_fields = ['cdkey', 'user__username']
    list_filter = ['status']


