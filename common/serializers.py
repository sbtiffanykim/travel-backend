from rest_framework import serializers
from rooms.models import Room
from users.models import User


class SimpleRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city")


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("pk", "name", "username", "profile_picture")
