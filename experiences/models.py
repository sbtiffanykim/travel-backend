from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=100)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    start_time = models.TimeField()
    end_time = models.TimeField()
    included_items = models.ManyToManyField("experiences.IncludedItem")
    categories = models.ForeignKey("categories.Category", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class IncludedItem(CommonModel):
    """What is included on an experience"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
