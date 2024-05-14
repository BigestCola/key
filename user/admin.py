from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, CDKey

# Profile 管理界面
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# CDKey 管理界面
class CDKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'created_by', 'validity_days', 'created_at', 'expires_at', 'is_used_field', 'used_by')
    list_filter = ('created_by', 'validity_days', 'is_used_field')
    search_fields = ('key', 'created_by__username')

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for cdkey in queryset:
            cdkey.delete()  # 这会触发模型的 delete 方法，可以在这里添加自定义逻辑
        self.message_user(request, "Selected CDKeys have been deleted.")
    delete_selected.short_description = "Delete selected CDKeys"

# User 管理界面
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'superior', 'is_active', 'is_staff', 'is_superuser', 'day_quota', 'monthly_quota', 'quota_updated_at']
    list_filter = ['user_type', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom fields', {'fields': ('user_type', 'superior', 'day_quota', 'monthly_quota')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'day_quota', 'monthly_quota'),
        }),
    )
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# 注册CDKey到管理界面
admin.site.register(CDKey, CDKeyAdmin)
