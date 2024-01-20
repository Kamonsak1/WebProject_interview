# Generated by Django 4.2.7 on 2024-01-20 11:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import interview.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                ("username", models.CharField(max_length=30, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("gender", models.CharField(max_length=20)),
                ("address", models.CharField(max_length=400)),
                ("postcode", models.CharField(max_length=20)),
                ("phone_number", models.CharField(max_length=10)),
                (
                    "citizen_id",
                    models.CharField(blank=True, max_length=13, null=True, unique=True),
                ),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Faculty",
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
                ("faculty", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Major",
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
                ("major", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Role",
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
                    "name",
                    models.CharField(
                        choices=[
                            ("Admin", "Admin"),
                            ("Manager", "Manager"),
                            ("Interviewer", "Interviewer"),
                            ("Student", "Student"),
                        ],
                        default="Admin",
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Round",
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
                ("academic_year", models.CharField(max_length=20)),
                ("round_name", models.CharField(max_length=20)),
                ("documents", models.CharField(blank=True, max_length=200, null=True)),
                ("active", models.BooleanField(blank=True, default=False, null=True)),
                (
                    "interview_time",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("line_Token", models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ScorePattern",
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
                ("pattern_name", models.CharField(max_length=100)),
                ("main_pattern", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TemporaryUser",
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
                ("citizen_id", models.CharField(max_length=13, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("birth_date", models.DateField(default=django.utils.timezone.now)),
                ("password", models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="ScoreTopic",
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
                ("topic_name", models.CharField(max_length=100)),
                ("max_score", models.PositiveIntegerField()),
                (
                    "score_detail",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "pattern_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Score_pattern",
                        to="interview.scorepattern",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Score",
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
                ("score", models.PositiveIntegerField()),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.scoretopic",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
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
                ("start_date", models.DateField(default=datetime.datetime.now)),
                ("end_date", models.DateField()),
                ("schedule_name", models.CharField(max_length=200)),
                ("schedule_content", models.TextField()),
                ("major", models.ManyToManyField(to="interview.major")),
                ("role", models.ManyToManyField(to="interview.role")),
                ("round", models.ManyToManyField(to="interview.round")),
            ],
        ),
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
                    "pattern",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.scorepattern",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="round",
            name="TemporaryUser",
            field=models.ManyToManyField(
                blank=True, related_name="round_temp_user", to="interview.temporaryuser"
            ),
        ),
        migrations.AddField(
            model_name="round",
            name="major",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="interview.major"
            ),
        ),
        migrations.AddField(
            model_name="round",
            name="manager",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="round",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="round_user", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="role",
            name="TemporaryUser",
            field=models.ManyToManyField(
                blank=True, related_name="roles", to="interview.temporaryuser"
            ),
        ),
        migrations.AddField(
            model_name="role",
            name="users",
            field=models.ManyToManyField(
                blank=True, related_name="roles", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="major",
            name="TemporaryUser",
            field=models.ManyToManyField(blank=True, to="interview.temporaryuser"),
        ),
        migrations.AddField(
            model_name="major",
            name="default_manager",
            field=models.ManyToManyField(
                blank=True, related_name="manager", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="major",
            name="faculty",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="interview.faculty"
            ),
        ),
        migrations.AddField(
            model_name="major",
            name="users",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="InterviewStatus",
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
                ("status", models.CharField(max_length=100)),
                ("reg_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.round",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_status",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InterviewNow",
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
                    "interviewer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interviewer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_student",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InterviewLink",
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
                ("link", models.CharField(max_length=300)),
                ("active", models.BooleanField(blank=True, default=False, null=True)),
                (
                    "round",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_round",
                        to="interview.round",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_link",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="faculty",
            name="TemporaryUser",
            field=models.ManyToManyField(blank=True, to="interview.temporaryuser"),
        ),
        migrations.AddField(
            model_name="faculty",
            name="users",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="Document",
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
                ("doc_name", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "document",
                    models.FileField(upload_to=interview.models.user_directory_path),
                ),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="interview.round",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Announcement",
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
                ("post_date", models.DateField(default=datetime.datetime.now)),
                ("expire_date", models.DateField(blank=True, null=True)),
                ("title", models.CharField(max_length=200)),
                ("announcement_content", models.TextField()),
                ("major", models.ManyToManyField(to="interview.major")),
                ("role", models.ManyToManyField(to="interview.role")),
                ("round", models.ManyToManyField(to="interview.round")),
            ],
        ),
    ]
