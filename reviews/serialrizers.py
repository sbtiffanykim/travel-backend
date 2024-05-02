from rest_framework import serializers
from .models import Review
from users.serializers import SimplifiedUserSerializer
from rooms.serializers import HostRoomSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "rating", "comments")


class HostReviewSerializer(serializers.ModelSerializer):

    room = HostRoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("room", "rating", "comments", "created_date")
