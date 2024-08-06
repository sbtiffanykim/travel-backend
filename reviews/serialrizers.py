from rest_framework import serializers
from .models import Review
from common.serializers import SimpleUserSerializer
from common.serializers import SimpleRoomSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "created_date", "rating", "comments")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation["user"]
        user_representation = dict(user_representation)
        user_representation["date_joined"] = instance.user.date_joined
        representation["user"] = user_representation

        return representation


class UserReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("rating", "comments", "created_date")


class HostReviewSerializer(serializers.ModelSerializer):

    room = SimpleRoomSerializer(read_only=True)
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "kind", "room", "rating", "comments", "created_date")
