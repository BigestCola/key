# Generated by Django 5.0.4 on 2024-05-16 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_rename_key_cdkey_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cdkey',
            old_name='code',
            new_name='key',
        ),
    ]