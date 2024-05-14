# Generated by Django 5.0.4 on 2024-05-14 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_cdkey_validity_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdkey',
            name='is_used_field',
            field=models.BooleanField(default=False, verbose_name='是否已使用'),
        ),
        migrations.AlterField(
            model_name='cdkey',
            name='validity_days',
            field=models.IntegerField(choices=[(1, '1 天'), (30, '30 天'), (90, '90 天'), (180, '180 天'), (365, '365 天'), (730, '730 天')], default=1),
        ),
    ]
