from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from categories.models import Category
from common.paginations import CustomPagination
from .models import Room, Amenity
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from reviews.serialrizers import ReviewSerializer
from media.serializers import PhotoSerializer
from reviews.models import Review
from media.models import Photo
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateBookingSerializer, HostBookingRecordSerializer


class RoomList(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")
        guests = request.query_params.get("guests")
        country = request.query_params.get("country")

        if check_in and check_out and guests and country:
            check_in = parse_date(check_in)
            check_out = parse_date(check_out)
            guests = int(guests)

            booked_rooms = Booking.objects.filter(Q(check_in__lt=check_out, check_out__gt=check_in)).values_list(
                "room", flat=True
            )

            rooms = (
                Room.objects.filter(country=country, max_capacity__gte=guests)
                .exclude(pk__in=booked_rooms)
                .order_by("pk")
            )

        else:
            rooms = Room.objects.all().order_by("pk")

        serializer = RoomListSerializer(self.paginate(rooms, request), many=True, context={"request": request})
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")

            # check input category
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError(f"The Category {category} does not exist")

            # add amenities
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


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

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
                            raise ParseError(f"Amenity {amenity_pk} not found")
                    room.amenities.set(amenities)
            return Response(RoomDetailSerializer(room, context={"request": request}).data)

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.host != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(self.paginate(room.reviews.all().order_by("-created_date"), request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, kind=Review.ReviewKindChoices.ROOM, room=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView, CustomPagination):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        amenities = room.amenities.all().order_by("pk")
        serializer = AmenitySerializer(self.paginate(amenities, request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})


class RoomPhotos(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = PhotoSerializer(self.paginate(room.photos.all().order_by("pk"), request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room, kind=Photo.PhotoKindChoices.ROOM)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AmenityList(APIView, CustomPagination):

    def get(self, request):
        all_amenities = Amenity.objects.all().order_by("pk")
        serializer = AmenitySerializer(self.paginate(all_amenities, request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

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


class RoomBookings(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        current_time = timezone.localtime(timezone.now()).date()
        room = self.get_object(pk=pk)

        # determine which serializer to use based on whether the user is the host or not
        if request.user == room.host:
            # if user is the host
            bookings = Booking.objects.filter(
                room__pk=room.pk, kind=Booking.BookingKindChoices.ROOM, check_in__gte=current_time
            ).order_by("check_in", "created_date")
            serializer = HostBookingRecordSerializer(self.paginate(bookings, request), many=True)

        else:
            # if user is not the host
            bookings = Booking.objects.filter(
                room__pk=room.pk, kind=Booking.BookingKindChoices.ROOM, check_in__gte=current_time
            ).order_by("check_in", "created_date")
            serializer = PublicBookingSerializer(self.paginate(bookings, request), many=True)

        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateBookingSerializer(data=request.data, context={"pk": pk})
        if serializer.is_valid():
            saved_booking = serializer.save(user=request.user, kind=Booking.BookingKindChoices.ROOM, room=room)
            serializer = PublicBookingSerializer(saved_booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
