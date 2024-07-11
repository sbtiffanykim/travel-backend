from rest_framework import serializers
from rooms.models import Room
from users.models import User
from experiences.models import Experience


class SimpleRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city")


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("pk", "name", "username", "profile_picture")


class SimpleExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ("pk", "name", "host", "country", "city")
