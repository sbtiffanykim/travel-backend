from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Inclusion, Experience
from .serializers import InclusionSerializer, ExperienceListSerializer, ExperienceDetailSerializer
from common.paginations import CustomPagination
from categories.models import Category


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
