from rest_framework import serializers
from rooms.models import Room
from users.models import User


class SimpleRoomSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("name", "country", "city", "room_type", "rating")

    def get_rating(self, room):
        return room.average_rating()


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "username", "profile_picture")
