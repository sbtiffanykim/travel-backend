from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):
    """Wishlist Model Definition"""

    name = models.CharField(max_length=100)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="wishlists")
    rooms = models.ManyToManyField("rooms.Room", related_name="wishlists", blank=True)
    experiences = models.ManyToManyField("experiences.Experience", related_name="wishlists", blank=True)

    def __str__(self):
        return self.name
