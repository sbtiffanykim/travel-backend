# Generated by Django 5.0.3 on 2024-04-02 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "experiences",
            "0004_experience_categories_alter_includeditem_description_and_more",
        ),
        ("rooms", "0005_room_categories"),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
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
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("file", models.ImageField(upload_to="")),
                ("description", models.CharField(max_length=150)),
                (
                    "kind",
                    models.CharField(
                        choices=[("room", "Room"), ("experience", "Experience")],
                        max_length=14,
                    ),
                ),
                (
                    "experience",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiences.experience",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rooms.room",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Video",
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
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("file", models.FileField(upload_to="")),
                (
                    "experience",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="experiences.experience",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]