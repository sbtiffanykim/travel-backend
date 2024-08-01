# Generated by Django 5.0.3 on 2024-07-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0009_room_max_capacity"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="bedrooms",
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]