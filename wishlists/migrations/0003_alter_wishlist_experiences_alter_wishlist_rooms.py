# Generated by Django 5.0.3 on 2024-04-30 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "experiences",
            "0004_experience_categories_alter_includeditem_description_and_more",
        ),
        ("rooms", "0008_alter_room_bathrooms_alter_room_number_of_rooms_and_more"),
        ("wishlists", "0002_alter_wishlist_experiences_alter_wishlist_rooms_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishlist",
            name="experiences",
            field=models.ManyToManyField(
                related_name="wishlists", to="experiences.experience"
            ),
        ),
        migrations.AlterField(
            model_name="wishlist",
            name="rooms",
            field=models.ManyToManyField(related_name="wishlists", to="rooms.room"),
        ),
    ]
