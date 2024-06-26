from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from common.serializers import SimpleRoomSerializer


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "experience_date")


class CreateBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "guests")

    def validate_check_in(self, value):
        current_date = timezone.localtime(timezone.now()).date()
        if current_date > value:
            raise serializers.ValidationError("Check in date must not be in the past")
        return value

    def validate_check_out(self, value):
        current_date = timezone.localtime(timezone.now()).date()
        if current_date > value:
            raise serializers.ValidationError("Check out date must not be in the past")
        return value

    def validate(self, data):
        room_pk = self.context.get("pk")
        if data.get("check_out") <= data.get("check_in"):
            raise serializers.ValidationError("Check-out data must not be smaller than check-in date")
        if Booking.objects.filter(
            check_in__lt=data.get("check_out"), check_out__gt=data.get("check_in"), room_id=room_pk
        ).exists():
            raise serializers.ValidationError("Room is not available during the selected period")
        return data


class BookingRecordSerializer(serializers.ModelSerializer):

    room = SimpleRoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "room")
