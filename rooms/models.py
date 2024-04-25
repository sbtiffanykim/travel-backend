from django.db import models
from common.models import CommonModel
from django.db.models import Avg


class Room(CommonModel):
    """Model Definition For Rooms"""

    class TypeChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    price = models.PositiveIntegerField()
    number_of_rooms = models.PositiveIntegerField(verbose_name="rooms")
    bathrooms = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_allowed = models.BooleanField(default=False)
    room_type = models.CharField(max_length=30, choices=TypeChoices, verbose_name="room type")
    amenities = models.ManyToManyField("rooms.Amenity", related_name="rooms")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rooms")
    category = models.ForeignKey(
        "categories.Category", on_delete=models.SET_NULL, blank=True, null=True, related_name="rooms"
    )

    def __str__(self):
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def average_rating(self):
        avg_rating = self.reviews.all().aggregate(Avg("rating"))["rating__avg"]
        if not avg_rating:
            return 0
        else:
            return round(avg_rating, 2)


class Amenity(CommonModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name
