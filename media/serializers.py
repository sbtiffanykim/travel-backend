from rest_framework import serializers
from .models import Photo, Video
from common.serializers import SimpleExperienceSerializer


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ("pk", "file", "description")


class VideoSerializer(serializers.ModelSerializer):

    experience = SimpleExperienceSerializer(read_only=True)

    class Meta:
        model = Video
        fields = ("pk", "file", "experience")
