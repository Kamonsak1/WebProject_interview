# Generated by Django 4.2.7 on 2024-01-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("interview", "0014_alter_temporaryuser_birth_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="temporaryuser",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
