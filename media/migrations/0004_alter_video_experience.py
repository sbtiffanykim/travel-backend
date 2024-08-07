# Generated by Django 5.0.3 on 2024-05-02 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0005_remove_experience_categories_experience_categories"),
        ("media", "0003_alter_photo_file_alter_video_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="experience",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video",
                to="experiences.experience",
            ),
        ),
    ]
