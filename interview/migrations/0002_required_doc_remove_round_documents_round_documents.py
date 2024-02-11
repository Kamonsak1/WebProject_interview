# Generated by Django 4.2.6 on 2024-02-11 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("interview", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Required_doc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("doc_name", models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name="round",
            name="documents",
        ),
        migrations.AddField(
            model_name="round",
            name="documents",
            field=models.ManyToManyField(
                blank=True, related_name="doc", to="interview.required_doc"
            ),
        ),
    ]
