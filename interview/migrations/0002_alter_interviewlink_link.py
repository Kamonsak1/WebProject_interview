# Generated by Django 4.2.6 on 2024-02-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interview", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="interviewlink",
            name="link",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]