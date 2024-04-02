from django.db import models
from common.models import CommonModel


class Room(CommonModel):
    """Model Definition For Rooms"""

    class TypeChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    price = models.PositiveBigIntegerField()
    number_of_rooms = models.PositiveBigIntegerField(verbose_name="rooms")
    bathrooms = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_allowed = models.BooleanField(default=False)
    room_type = models.CharField(max_length=30, choices=TypeChoices, verbose_name="room type")
    amenities = models.ManyToManyField("rooms.Amenity")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Amenity(CommonModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    icon = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name
