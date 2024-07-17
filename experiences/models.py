from datetime import timedelta, datetime, time
from django.db import models
from django.db.models import Q, F, Avg, Sum, Value
from django.db.models.functions import Coalesce
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
    duration = models.DurationField(default=timedelta(hours=2))

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

    # create sessions based on start_date, end_date, start_time, end_time, and duration
    def create_sessions(self):

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

    def get_available_sessions(self, check_in, check_out, guests):

        available_sessions = self.sessions.filter(
            date__range=[check_in, check_out],
        ).annotate(
            total_booked=Coalesce(
                Sum(
                    "bookings__guests",
                    filter=Q(
                        bookings__is_cancelled=False,
                        bookings__approval_status__in=[
                            Booking.BookingApprovalStatusChoices.APPROVED,
                            Booking.BookingApprovalStatusChoices.PENDING,
                        ],
                    ),
                ),
                Value(0),
            )
        )

        if guests:
            available_sessions = available_sessions.filter(
                Q(experience__max_capacity__gte=guests)
                & Q(experience__max_capacity__gt=models.F("total_booked") + guests)
            )
        else:
            available_sessions = available_sessions.filter(experience__max_capacity__gt=models.F("total_booked"))

        return available_sessions.distinct()

    @classmethod
    def get_available_experiences(cls, check_in, check_out, guests, country):
        experiences = cls.objects.filter(country=country)
        available_experiences = []

        for experience in experiences:
            available_sessions = experience.get_available_sessions(check_in, check_out, guests)
            if available_sessions.exists():
                available_experiences.append(experience)

        # print(f"experiences: {available_experiences}")
        return cls.objects.filter(id__in=[exp.id for exp in available_experiences])


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
            is_cancelled=False,
            approval_status__in=[
                Booking.BookingApprovalStatusChoices.APPROVED,
                Booking.BookingApprovalStatusChoices.PENDING,
            ],
        )
        total_booked = bookings.aggregate(Sum("guests"))["guests__sum"] or 0
        return self.experience.max_capacity - total_booked if self.experience.max_capacity else None


class Inclusion(CommonModel):
    """What is included on an experience"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
