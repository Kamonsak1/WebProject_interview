# Generated by Django 4.2.6 on 2023-12-02 19:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interview", "0004_scoretopic_score_detail"),
    ]

    operations = [
        migrations.AddField(
            model_name="round",
            name="documents",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
