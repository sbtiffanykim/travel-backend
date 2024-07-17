# Generated by Django 5.0.3 on 2024-07-17 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0012_experience_end_date_experience_start_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="duration",
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
    ]
