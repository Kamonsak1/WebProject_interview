# Generated by Django 4.2.6 on 2023-12-10 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("interview", "0010_remove_scoretopic_round_delete_roundscore"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoundScore",
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
                (
                    "Round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.round",
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.scoretopic",
                    ),
                ),
            ],
        ),
    ]
