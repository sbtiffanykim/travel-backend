# Generated by Django 5.0.3 on 2024-07-12 06:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0010_remove_experience_thumnail_experience_thumbnail"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="duration",
            field=models.DurationField(default=datetime.timedelta(seconds=3600)),
        ),
    ]
