# Generated by Django 5.0.4 on 2024-05-16 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_rename_code_cdkey_key'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='user_custom',
        ),
    ]