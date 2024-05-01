from rest_framework import serializers
from .models import Room, Amenity
from users.serializers import SimplifiedUserSerializer
from reviews.serialrizers import ReviewSerializer
from categories.serializers import CategorySerializer
from media.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ("pk", "name", "description", "icon")


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "rating", "is_owner", "photos")

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
    photos = PhotoSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.average_rating()

    def get_is_owner(self, room):
        return room.host == self.context.get("request").user

    def get_is_liked(self, room):
        request = self.context.get("request")
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()


class HostRoomSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("name", "country", "city", "room_type", "rating")

    def get_rating(self, room):
        return room.average_rating()
