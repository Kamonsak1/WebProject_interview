# Generated by Django 4.2.7 on 2024-02-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0002_required_doc_remove_round_documents_round_documents"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name2",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name2",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
