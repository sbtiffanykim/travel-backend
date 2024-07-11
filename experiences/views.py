from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Inclusion, Experience
from .serializers import InclusionSerializer, ExperienceListSerializer, ExperienceDetailSerializer
from common.paginations import CustomPagination
from categories.models import Category
from media.models import Photo, Video
from reviews.serialrizers import ReviewSerializer
from media.serializers import PhotoSerializer, VideoSerializer


class InclusionList(APIView, CustomPagination):

    def get(self, request):
        all_inclusions = Inclusion.objects.all().order_by("id")
        serializer = InclusionSerializer(self.paginate(all_inclusions, request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request):
        serializer = InclusionSerializer(data=request.data)
        if serializer.is_valid():
            new_item = serializer.save()
            return Response(InclusionSerializer(new_item).data)
        else:
            return Response(serializer.errors)


class InclusionDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Inclusion.objects.get(pk=pk)
        except Inclusion.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = InclusionSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = InclusionSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            updated_item = serializer.save()
            return Response(InclusionSerializer(updated_item).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceList(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(self.paginate(all_experiences, request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pks = request.data.get("categories")
            inclusions_pks = request.data.get("inclusions")

            if not category_pks:
                raise ParseError("Category is required")

            # check input categories
            try:
                categories = []
                for category_pk in category_pks:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The Category shoud be 'experience'")
                    categories.append(category)
            except Category.DoesNotExsit:
                raise ParseError(f"The Category {category} does not exist")

            # add inclusions
            try:
                with transaction.atomic():
                    new_experience = serializer.save(host=request.user)
                    new_experience.categories.set(categories)  # add multiple categories
                    if inclusions_pks:
                        for inclusion_pk in inclusions_pks:
                            inclusion = Inclusion.objects.get(pk=inclusion_pk)
                            new_experience.inclusions.add(inclusion)

            except Inclusion.DoesNotExist:
                raise ParseError("Inclusion not found")
            except Exception as e:
                raise ParseError(e)

            serializer = ExperienceDetailSerializer(new_experience, context={"request": request})
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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
                item_pks = request.data.get("inclusions")
                if item_pks:
                    items = []
                    for item_pk in item_pks:
                        try:
                            item = Inclusion.objects.get(pk=item_pk)
                            items.append(item)
                        except Inclusion.DoesNotExist:
                            raise ParseError(f"Item {item_pk} does not found")
                    updated_experience.inclusions.set(items)

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
        items = experience.inclusions.all()
        serializer = InclusionSerializer(items, many=True)
        return Response(serializer.data)


class ExperienceReviews(APIView, CustomPagination):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ReviewSerializer(self.paginate(experience.reviews.all(), request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})


class ExperiencePhotos(APIView, CustomPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = PhotoSerializer(self.paginate(experience.photos.all(), request), many=True)
        return Response({"page": self.link_info, "content": serializer.data})

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:  # not authenticated
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience, kind=Photo.PhotoKindChoices.EXPERIENCE)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:  # not a valid photo
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ExperienceThumbnailSelector(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def put(self, request, pk, photo_pk):
        experience = self.get_object(pk)

        # check if the request user is the host of the experience
        if request.user != experience.host:
            raise PermissionDenied

        # retrieve the photo associated with the experience
        try:
            photo = Photo.objects.get(pk=photo_pk, experience=experience)
        except Photo.DoesNotExist:
            raise NotFound(f"Photo with id {photo_pk} not found for this experience")

        # store the previous thumbnail
        previous_thumbnail = experience.thumbnail

        # set the new thumbnail
        experience.thumbnail = photo
        experience.save()

        if previous_thumbnail and previous_thumbnail != photo:
            message = "Thumbnail updated successfully"
        else:
            message = "Thumbnail set successfully"

        serializer = PhotoSerializer(photo)

        return Response({"message": message, "thumbnail": serializer.data})


class ExperienceVideo(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_experience_video(self, experience):
        try:
            return experience.video
        except Video.DoesNotExist:
            return

    def get(self, request, pk):
        experience = self.get_object(pk)
        if not self.get_experience_video(experience):
            return Response(status=HTTP_204_NO_CONTENT)
        serializer = VideoSerializer(experience.video)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:  # not authenticated
            raise PermissionDenied
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            if self.get_experience_video(experience):  # video already exists
                raise ParseError("Only 1 video allowed for an experience")
            video = serializer.save(experience=experience)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        else:  # not a valid video
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
