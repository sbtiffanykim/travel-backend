from rest_framework import serializers
from .models import Experience, IncludedItem
from common.serializers import SimpleUserSerializer
from categories.serializers import CategorySerializer
from reviews.serialrizers import ReviewSerializer


class IncludedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncludedItem
        fields = ("pk", "name", "details", "description")


class ExperienceListSerializer(serializers.ModelSerializer):

    total_reviews = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()
    host = SimpleUserSerializer()

    class Meta:
        model = Experience
        fields = ("pk", "name", "country", "host", "price", "total_reviews", "rating_average", "photos", "video")

    def get_total_reviews(self, experience):
        return experience.total_reviews()

    def get_rating_average(self, experience):
        return experience.rating_average()


class ExperienceDetailSerializer(serializers.ModelSerializer):

    included_items = IncludedItemSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    host = SimpleUserSerializer()
    reviews = ReviewSerializer(many=True)
    total_reviews = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()

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
            "included_items",
            "categories",
            "total_reviews",
            "reviews",
            "photos",
            "video",
        )

    def get_rating_average(self, experience):
        return experience.rating_average()

    def get_total_reviews(self, experiences):
        return experiences.total_reviews()
