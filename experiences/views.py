from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import IncludedItem, Experience
from .serializers import IncludedItemSerializer, ExperienceListSerializer, ExperienceDetailSerializer
from categories.models import Category


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
            return IncludedItem.objects.get(pk=pk)
        except IncludedItem.DoesNotExist:
            raise NotFound

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

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        # if serializer.is_valid():
        #     categories = request.data.get("categories")
        #     print(categories, type(categories))
        # else:
        #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)

        if request.user != experience.host:
            raise PermissionDenied

        serializer = ExperienceDetailSerializer(experience, data=request.data, partial=True)

        if serializer.is_valid():
            updated_experience = serializer.save()

            with transaction.atomic():
                # check categories
                category_pks = request.data.get("categories")
                if category_pks:
                    categories = []
                    for category_pk in category_pks:
                        try:
                            category = Category.objects.get(pk=category_pk)
                            if category.kind != category.CategoryKindChoices.EXPERIENCES:
                                raise ParseError(f"Category {category_pk} must be in 'experience' Category")
                            categories.append(category)
                        except Category.DoesNotExist:
                            raise ParseError(f"Category {category_pk} does not found")
                    updated_experience.categories.set(categories)

                # check included items
                item_pks = request.data.get("included_items")
                if item_pks:
                    items = []
                    for item_pk in item_pks:
                        try:
                            item = IncludedItem.objects.get(pk=item_pk)
                            items.append(item)
                        except IncludedItem.DoesNotExist:
                            raise ParseError(f"Item {item_pk} does not found")
                    updated_experience.included_items.set(items)

            return Response(ExperienceDetailSerializer(updated_experience, context={"request": request}).data)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceItems(APIView):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        items = experience.included_items.all()
        serializer = IncludedItemSerializer(items, many=True)
        return Response(serializer.data)
