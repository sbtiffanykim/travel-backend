from rest_framework import serializers
from .models import Experience, IncludedItem


class IncludedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncludedItem
        fields = "__all__"
