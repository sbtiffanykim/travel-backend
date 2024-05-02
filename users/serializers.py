from rest_framework import serializers
from .models import User


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "profile_picture",
            "date_joined",
            "last_login",
            "is_host",
            "gender",
            "language",
            "currency",
        )


class PublicUserSerializer(serializers.ModelSerializer):
    # how many room the user has / reviews that the user left / past travel records

    class Meta:
        model = User
        fields = "__all__"
