from rest_framework import serializers
from .models import User
from rooms.models import Room
from rooms.serializers import HostRoomSerializer
from reviews.models import Review
from reviews.serialrizers import HostReviewSerializer, UserReviewSerializer
from bookings.models import Booking
from bookings.serializers import BookingRecordSerializer


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "profile_picture",
            "date_joined",
            "last_login",
            "is_host",
            "gender",
            "language",
            "currency",
        )


class PublicUserSerializer(serializers.ModelSerializer):
    # past travel records

    recent_reviews = serializers.SerializerMethodField()
    host_reviews = serializers.SerializerMethodField()
    rooms = serializers.SerializerMethodField()
    booking_records = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "gender",
            "email",
            "profile_picture",
            "recent_reviews",
            "rooms",
            "host_reviews",
            "booking_records",
            "language",
            "currency",
        )

    def get_recent_reviews(self, user):
        recent_reviews = user.reviews.all().order_by("-created_date")[:5]
        return UserReviewSerializer(recent_reviews, many=True).data

    def get_rooms(self, user):
        rooms = Room.objects.filter(host=user)
        return HostRoomSerializer(rooms, many=True).data

    def get_host_reviews(self, user):
        host_reviews = Review.objects.filter(room__host=user).order_by("room__pk")
        return HostReviewSerializer(host_reviews, many=True).data

    def get_booking_records(self, user):
        booking_records = Booking.objects.filter(user=user).order_by("-check_out")
        # [total_num_of_bookings, booking_lists]
        return [booking_records.count(), BookingRecordSerializer(booking_records, many=True).data]
