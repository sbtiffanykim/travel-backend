from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from common.models import CommonModel


class Review(CommonModel):
    """Review from a user to a room / experience"""

    class ReviewKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("experience", "Experience")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    kind = models.CharField(max_length=14, choices=ReviewKindChoices.choices, default="room")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], help_text="Please choose between 0 and 5"
    )
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.rating}"
