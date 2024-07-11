from rest_framework import serializers
from .models import Experience, Inclusion
from common.serializers import SimpleUserSerializer
from categories.serializers import CategorySerializer
from reviews.serialrizers import ReviewSerializer
from media.serializers import PhotoSerializer, VideoSerializer


class InclusionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inclusion
        fields = ("pk", "name", "details", "description")


class ExperienceListSerializer(serializers.ModelSerializer):

    total_reviews = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()
    host = SimpleUserSerializer()
    photos = PhotoSerializer(many=True, read_only=True)
    video = VideoSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = ("pk", "name", "country", "host", "price", "total_reviews", "rating_average", "photos", "video")

    def get_total_reviews(self, experience):
        return experience.total_reviews()

    def get_rating_average(self, experience):
        return experience.rating_average()


class ExperienceDetailSerializer(serializers.ModelSerializer):

    inclusions = InclusionSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    host = SimpleUserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    video = VideoSerializer(read_only=True)
    total_reviews = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()
    thumbnail = PhotoSerializer(read_only=True)

    class Meta:
        model = Experience
        # exclude = ("created_date", "updated_date")
        fields = (
            "pk",
            "name",
            "country",
            "host",
            "price",
            "max_capacity",
            "rating_average",
            "inclusions",
            "categories",
            "total_reviews",
            "reviews",
            "thumbnail",
            "photos",
            "video",
        )

    def get_rating_average(self, experience):
        return experience.rating_average()

    def get_total_reviews(self, experiences):
        return experiences.total_reviews()
