from rest_framework import serializers
from rooms.models import Room


class SimpleRoomSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("name", "country", "city", "room_type", "rating")

    def get_rating(self, room):
        return room.average_rating()
