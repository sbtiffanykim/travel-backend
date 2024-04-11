from rest_framework import serializers
from .models import Room, Amenity
from users.serializers import SimplifiedUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ("pk", "name", "description", "icon")


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "rating", "is_owner")

    def get_rating(self, room):
        return room.average_rating()

    def get_is_owner(self, room):
        return room.host == self.context.get("request").user


class RoomDetailSerializer(serializers.ModelSerializer):

    host = SimplifiedUserSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.average_rating()

    def get_is_owner(self, room):
        return room.host == self.context.get("request").user
