from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from categories.models import Category
from .models import Room, Amenity


class Rooms(APIView):

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("The Category does not exist")
                try:
                    with transaction.atomic():
                        new_room = serializer.save(host=request.user, category=category)
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            new_room.amenities.add(amenity)
                        serializer = RoomDetailSerializer(new_room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = RoomDetailSerializer(self.get_object(pk), context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.host != request.user:
            raise PermissionDenied

        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            room = serializer.save()

            with transaction.atomic():
                # check the category
                category_pk = request.data.get("category")
                if category_pk:
                    try:
                        category = Category.objects.get(pk=category_pk)
                        if category.kind != Category.CategoryKindChoices.ROOMS:
                            raise ParseError("The category should be 'rooms'")
                        room.category = category
                    except Category.DoesNotExist:
                        raise ParseError("Category not found")

                # check amenities
                amenity_pks = request.data.get("amenities")
                if amenity_pks:
                    amenities = []
                    for amenity_pk in amenity_pks:
                        try:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            amenities.append(amenity)
                        except Amenity.DoesNotExist:
                            raise ParseError("Amenity not found")
                    room.amenities.set(amenities)
            return Response(RoomDetailSerializer(room, context={"request": request}).data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.host != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            amenity = Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
        return amenity

    def get(self, request, pk):
        serializer = AmenitySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = AmenitySerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
