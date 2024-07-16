from datetime import timedelta, datetime, time
from django.db import models
from django.db.models import Avg
from common.models import CommonModel
from bookings.models import Booking


class Experience(CommonModel):
    """Experience Model Definition"""

    name = models.CharField(max_length=100)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=80, default="")
    address = models.CharField(max_length=250)
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    inclusions = models.ManyToManyField("experiences.Inclusion", related_name="experiences")
    categories = models.ManyToManyField("categories.Category", related_name="experiences")
    max_capacity = models.PositiveIntegerField(blank=True, null=True)  # number of guests allowed
    thumbnail = models.ForeignKey(
        "media.Photo", on_delete=models.SET_NULL, null=True, blank=True, related_name="thumbnail"
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(default=timedelta(hours=1))

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

    def create_sessions(self):
        # create sessions based on start_date, end_date, start_time, end_time, and duration

        current_date = self.start_date
        while current_date <= self.end_date:
            current_time = self.start_time
            while current_time < self.end_time:
                # calculate the end time of the current session by adding the duration to the current start time
                session_end_time = (datetime.combine(current_date, current_time) + self.duration).time()

                if session_end_time <= self.end_time:
                    ExperienceSession.objects.create(
                        experience=self,
                        date=current_date,
                        start_time=current_time,
                        end_time=session_end_time,
                        capacity=self.max_capacity,
                    )
                    # update current_time
                    current_time = session_end_time
                else:
                    break

            # move to the next day
            current_date += timedelta(days=1)


class ExperienceSession(CommonModel):
    """Experience Session Model Definition"""

    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    # calculate remaining slots
    def available_slots(self):
        bookings = self.bookings.filter(
            experience_session=self,
            is_cancelled=False,
            approval_status__in=[
                Booking.BookingApprovalStatusChoices.APPROVED,
                Booking.BookingApprovalStatusChoices.PENDING,
            ],
        )
        total_booked = sum(booking.guests for booking in bookings)
        return self.max_capacity - total_booked if self.max_capacity else None


class Inclusion(CommonModel):
    """What is included on an experience"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
