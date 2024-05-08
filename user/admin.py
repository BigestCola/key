# user/admin.py

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_type', 'superior', 'is_active']  # 将 'status' 替换为 'is_active'
    list_filter = ['user_type', 'is_active']  # 将 'status' 替换为 'is_active'
    search_fields = ['username']