# Generated by Django 4.1.5 on 2023-01-18 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=500)),
                ("type", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=500)),
                ("tag", models.CharField(max_length=30)),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("FAIBLE", "Faible"),
                            ("MOYENNE", "Moyenne"),
                            ("ELEVEE", "Elevée"),
                        ],
                        max_length=30,
                        verbose_name="Priorité",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AFAIRE", "A faire"),
                            ("ENCOURS", "En cours"),
                            ("TERMINE", "Terminé"),
                        ],
                        max_length=30,
                    ),
                ),
                ("project_id", models.IntegerField()),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "assignee",
                    models.ForeignKey(
                        default=models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name="issue_author",
                            to=settings.AUTH_USER_MODEL,
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_assignee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contributor",
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
                ("user_id", models.IntegerField()),
                ("project_id", models.IntegerField()),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("AUTHOR", "Auteur"),
                            ("CONTRIBUTOR", "Collaborateur"),
                        ],
                        max_length=30,
                        verbose_name="Rôle",
                    ),
                ),
            ],
            options={
                "unique_together": {("user_id", "project_id")},
            },
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("description", models.CharField(max_length=500)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="projects.issue"
                    ),
                ),
            ],
        ),
    ]
