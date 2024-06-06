# Generated by Django 5.0.6 on 2024-06-05 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_alter_project_slug"),
        (
            "questions",
            "0003_question_max_question_min_question_open_lower_bound_and_more",
        ),
        ("scoring", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userweights",
            name="user",
        ),
        migrations.CreateModel(
            name="LeaderboardEntry",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited_at", models.DateTimeField(auto_now=True)),
                (
                    "leaderboard_type",
                    models.CharField(
                        choices=[
                            ("metaculus_points", "metaculus_points"),
                            ("peer_accuracy", "peer_accuracy"),
                            ("baseline_accuracy", "baseline_accuracy"),
                            ("peer_spot_forecast", "peer_spot_forecast"),
                            ("baseline_spot_forecast", "baseline_spot_forecast"),
                        ],
                        max_length=200,
                    ),
                ),
                ("score", models.FloatField()),
                ("medal", models.CharField(max_length=200, null=True)),
                ("calculated_on", models.DateTimeField(auto_now_add=True)),
                (
                    "for_project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
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
            options={
                "abstract": False,
            },
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited_at", models.DateTimeField(auto_now=True)),
                ("score", models.FloatField()),
                (
                    "score_type",
                    models.CharField(
                        choices=[
                            ("metaculus_points", "metaculus_points"),
                            ("peer_accuracy", "peer_accuracy"),
                            ("baseline_accuracy", "baseline_accuracy"),
                            ("peer_spot_forecast", "peer_spot_forecast"),
                            ("baseline_spot_forecast", "baseline_spot_forecast"),
                        ],
                        max_length=200,
                    ),
                ),
                (
                    "for_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="questions.question",
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
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserWeight",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("edited_at", models.DateTimeField(auto_now=True)),
                ("calculated_on", models.DateTimeField(auto_now_add=True)),
                ("weight", models.FloatField(default=1)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="Leaderboard",
        ),
        migrations.DeleteModel(
            name="UserWeights",
        ),
    ]