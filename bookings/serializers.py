from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from experiences.models import Experience, ExperienceSession
from common.serializers import SimpleUserSerializer


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ("pk", "check_in", "check_out", "experience_date")


class HostBookingRecordSerializer(serializers.ModelSerializer):
    """Only for the host"""

    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "user",
            "check_in",
            "check_out",
            "experience_date",
            "guests",
            "approval_status",
            "is_cancelled",
        )


class UserBookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("pk", "room", "experience", "check_in", "check_out", "experience_date")


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


class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_date = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = ("pk", "experience_session", "guests", "experience_date")

    def validate(self, data):
        experience_pk = self.context.get("pk")
        session = data.get("experience_session")
        input_guests = data.get("guests")

        experience = Experience.objects.get(pk=experience_pk)

        if not session or session.experience != experience:
            raise serializers.ValidationError("Invalid sesion selected for this experience")

        if input_guests > session.available_slots():
            raise serializers.ValidationError("Not enough slots available for the selected time")

        return data
