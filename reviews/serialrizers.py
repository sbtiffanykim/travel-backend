from rest_framework import serializers
from .models import Review
from users.serializers import SimplifiedUserSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "rating", "comments")
