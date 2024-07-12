from django.db import models
from common.models import CommonModel


class Booking(CommonModel):
    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")
    
    class BookingApprovalStatusChoices(models.TextChoices):
        PENDING = ('pending', 'Pending')
        APPROVED = ('approved', 'Approved')
        DENIDED = ('denied', 'Denied')

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='bookings')
    kind = models.CharField(max_length=14, choices=BookingKindChoices.choices)
    room = models.ForeignKey("rooms.Room", on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings')  # one-to-many
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.SET_NULL, blank=True, null=True, related_name='bookings'
    )
    check_in = models.DateField(blank=True, null=True)
    check_out = models.DateField(blank=True, null=True)
    experience_date = models.DateTimeField(blank=True, null=True)
    guests = models.PositiveIntegerField()
    approval_status = models.CharField(max_length = 20, choices=BookingApprovalStatusChoices.choices, default=BookingApprovalStatusChoices.PENDING)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'Booking {self.kind.title()}: {self.room if self.kind=='room' else self.experience} by {self.user}'
