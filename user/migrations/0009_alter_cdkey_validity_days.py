# Generated by Django 5.0.4 on 2024-05-08 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_cdkey_used_at_cdkey_validity_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdkey',
            name='validity_days',
            field=models.IntegerField(choices=[(1, '1 天'), (31, '31 天')], default=1),
        ),
    ]
