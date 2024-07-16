from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "kind", "experience_session", "room", "check_in", "check_out", "experience_date", "guests")
    list_filter = ("kind",)
