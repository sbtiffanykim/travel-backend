from django.contrib import admin
from .models import Experience, Inclusion, ExperienceSession


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("name", "host", "country", "city", "price")
    list_filter = ("country", "city")


@admin.register(Inclusion)
class InclusionAdmin(admin.ModelAdmin):
    list_display = ("name", "details")


@admin.register(ExperienceSession)
class ExperienceSessionAdmin(admin.ModelAdmin):
    list_display = ("experience", "date", "start_time", "end_time", "is_available")
    list_filter = ("experience",)
