# Generated by Django 4.2.4 on 2023-11-10 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0002_alter_faculty_temporaryuser_alter_faculty_users_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="temporaryuser",
            name="password",
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
