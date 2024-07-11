from django.contrib import admin
from .models import Experience, Inclusion


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "country", "city", "price")
    list_filter = ("country", "city")


@admin.register(Inclusion)
class InclusionAdmin(admin.ModelAdmin):
    list_display = ("name", "details")
