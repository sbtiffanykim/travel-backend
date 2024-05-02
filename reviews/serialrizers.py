from rest_framework import serializers
from .models import Review
from common.serializers import SimpleUserSerializer
from common.serializers import SimpleRoomSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "rating", "comments")


class HostReviewSerializer(serializers.ModelSerializer):

    room = SimpleRoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("room", "rating", "comments", "created_date")
