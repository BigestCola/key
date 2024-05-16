# Generated by Django 5.0.4 on 2024-05-16 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdkey', '0003_alter_cdkey_table'),
        ('user', '0017_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdkeyextractrecord',
            name='cdkey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extract_records', to='user.cdkey'),
        ),
        migrations.DeleteModel(
            name='CDKey',
        ),
    ]
