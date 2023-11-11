# Generated by Django 4.2.4 on 2023-11-11 05:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0004_major_temporaryuser_major_users_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="major", name="default_manager",),
        migrations.AlterField(
            model_name="major",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="user", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="major",
            name="default_manager",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="manager",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
