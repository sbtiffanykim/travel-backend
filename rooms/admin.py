from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="10 percent discount")
def modify_prices(model_admin, request, queryset):
    for query in queryset:
        item = Room.objects.get(pk=query.pk)
        item.price *= 0.9
        item.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (modify_prices,)

    list_display = ("name", "country", "city", "price", "host", "total_amenities", "average_rating")
    list_filter = ("country", "city")
    search_fields = ("name",)
    search_help_text = "Search room with its name"


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
