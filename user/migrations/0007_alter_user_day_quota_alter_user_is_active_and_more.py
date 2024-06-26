# Generated by Django 5.0.4 on 2024-05-08 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='day_quota',
            field=models.IntegerField(default=0, verbose_name='日配额'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否激活'),
        ),
        migrations.AlterField(
            model_name='user',
            name='monthly_quota',
            field=models.IntegerField(default=0, verbose_name='月度配额'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', '管理员'), ('agent', '代理')], default='agent', max_length=50, verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='user',
            name='superior',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to=settings.AUTH_USER_MODEL, verbose_name='上级'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.SmallIntegerField(choices=[(1, '管理员'), (2, '一级代理'), (3, '二级代理')], default=3, verbose_name='用户类型'),
        ),
    ]
