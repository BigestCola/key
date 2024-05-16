# cdkey/admin.py
from django.contrib import admin
from user.models import CDKey

@admin.register(CDKey)
class CDKeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'validity_days', 'created_by', 'created_at', 'expires_at', 'is_used_field']
    search_fields = ['key', 'created_by__username']
    list_filter = ['validity_days', 'is_used_field']


