# Generated by Django 4.2.6 on 2023-12-02 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interview", "0007_interviewstatus_reg_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="round",
            name="interview_time",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]