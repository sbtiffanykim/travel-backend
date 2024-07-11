# Generated by Django 5.0.3 on 2024-07-11 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_alter_category_options_rename_type_category_kind"),
        ("experiences", "0006_experience_max_capacity"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="IncludedItem",
            new_name="Inclusion",
        ),
        migrations.RemoveField(
            model_name="experience",
            name="included_items",
        ),
        migrations.AddField(
            model_name="experience",
            name="inclusions",
            field=models.ManyToManyField(
                related_name="experiences", to="experiences.inclusion"
            ),
        ),
        migrations.AlterField(
            model_name="experience",
            name="categories",
            field=models.ManyToManyField(
                related_name="experiences", to="categories.category"
            ),
        ),
    ]
