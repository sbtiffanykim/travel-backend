from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(max_length=100)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="wishlists")
    rooms = models.ManyToManyField("rooms.Room", blank=True, related_name="wishlists")
    experiences = models.ManyToManyField("experiences.Experience", blank=True, related_name="wishlists")

    def __str__(self):
        return self.name
