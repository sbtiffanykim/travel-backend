from datetime import timedelta
from django.db import models
from django.db.models import Avg
from common.models import CommonModel


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=100)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    address = models.CharField(max_length=250)
    price = models.PositiveBigIntegerField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta(hours=1))
    description = models.TextField()
    inclusions = models.ManyToManyField("experiences.Inclusion", related_name="experiences")
    categories = models.ManyToManyField("categories.Category", related_name="experiences")
    max_capacity = models.PositiveIntegerField(blank=True, null=True)  # number of guests allowed
    thumbnail = models.ForeignKey(
        "media.Photo", on_delete=models.SET_NULL, null=True, blank=True, related_name="thumbnail"
    )

    def __str__(self):
        return self.name

    def total_reviews(self):
        return self.reviews.count()

    def rating_average(self):
        rating_avg = self.reviews.all().aggregate(Avg("rating"))["rating__avg"]
        if not rating_avg:
            return 0
        else:
            return round(rating_avg, 2)

    # remaining seats


class Inclusion(CommonModel):
    """What is included on an experience"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
