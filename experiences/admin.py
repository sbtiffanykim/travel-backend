from django.contrib import admin
from .models import Experience, IncludedItem


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "country", "city", "price")
    list_filter = ("country", "city")


@admin.register(IncludedItem)
class IncludedItemAdmin(admin.ModelAdmin):
    list_display = ("name", "details")
