# Generated by Django 4.2.13 on 2024-06-14 13:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_core', '0002_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
