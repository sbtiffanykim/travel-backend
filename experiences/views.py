from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from .models import IncludedItem, Experience
from .serializers import IncludedItemSerializer, ExperienceListSerializer, ExperienceDetailSerializer


class IncludedItems(APIView):

    def get(self, request):
        all_included_items = IncludedItem.objects.all()
        serializer = IncludedItemSerializer(all_included_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncludedItemSerializer(data=request.data)
        if serializer.is_valid():
            new_item = serializer.save()
            return Response(IncludedItemSerializer(new_item).data)
        else:
            return Response(serializer.errors)


class IncludedItemDetail(APIView):

    def get_object(self, pk):
        try:
            included_item = IncludedItem.objects.get(pk=pk)
        except IncludedItem.DoesNotExist:
            raise NotFound
        return included_item

    def get(self, request, pk):
        serializer = IncludedItemSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = IncludedItemSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_item = serializer.save()
            return Response(IncludedItemSerializer(updated_item).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceLists(APIView):
    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(all_experiences, many=True)
        return Response(serializer.data)


class ExperienceDetail(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)
