from rest_framework import serializers
from .models import Room, Amenity
from common.serializers import SimpleUserSerializer
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
    number_of_reviews = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "description",
            "room_type",
            "bedrooms",
            "price",
            "rating",
            "number_of_reviews",
            "is_owner",
            "photos",
        )

    def get_room_type(self, room):
        room_type = room.room_type
        room_type = room_type.replace("_", " ").title()
        return room_type

    def get_rating(self, room):
        return room.rating_average()

    def get_number_of_reviews(self, room):
        return room.reviews.count()

    def get_is_owner(self, room):
        return room.host == self.context.get("request").user


class RoomDetailSerializer(serializers.ModelSerializer):

    host = SimpleUserSerializer(read_only=True)
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
        return room.rating_average()

    def get_is_owner(self, room):
        return room.host == self.context.get("request").user

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()
        return False


class HostRoomSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "room_type", "rating", "total_reviews")

    def get_rating(self, room):
        return room.rating_average()

    def get_total_reviews(self, room):
        return room.total_reviews()
