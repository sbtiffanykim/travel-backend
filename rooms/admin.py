from django.contrib import admin
from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city", "price", "host", "total_amenities")
    list_filter = ("country", "city")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
