from rest_framework.serializers import ModelSerializer
from .models import User


class SimplifiedUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "username", "profile_picture")
