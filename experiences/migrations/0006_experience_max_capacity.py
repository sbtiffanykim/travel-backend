# Generated by Django 5.0.3 on 2024-05-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0005_remove_experience_categories_experience_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="max_capacity",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
