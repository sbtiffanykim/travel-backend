from django.db import models
from common.models import CommonModel


class Booking(CommonModel):
    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='bookings')
    kind = models.CharField(max_length=14, choices=BookingKindChoices.choices)
    room = models.ForeignKey("rooms.Room", on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings')  # one-to-many
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings'
    )  # one-to-many
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    experience_date = models.DateTimeField(blank=True, null=True)
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f'Booking {self.kind.title()}: {self.room if self.kind=='room' else self.experience} by {self.user}'
