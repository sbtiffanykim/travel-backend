import jwt
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from . import serializers
from common.serializers import SimpleRoomSerializer, SimpleUserSerializer
from rooms.serializers import HostRoomSerializer
from reviews.models import Review
from reviews.serialrizers import UserReviewSerializer, HostReviewSerializer


class CreateAccount(APIView):

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required")
        try:
            validate_password(password)
        except Exception as e:
            raise ParseError(e)
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            created_user = serializer.save()
            created_user.set_password(password)
            created_user.save()
            serializer = serializers.PrivateUserSerializer(created_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PrivateUserProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.PrivateUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_profile = serializer.save()
            serializer = serializers.PrivateUserSerializer(updated_profile)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUserProfile(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if not old_password or not new_password:
            raise ParseError
        if new_password != confirm_password:
            raise ValidationError("Passwords do not match")
        try:
            validate_password(new_password)
        except Exception as e:
            raise ParseError(e)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"login": "success"})
        else:
            return Response({"Error": "Wrong Password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"logout": "success"})


class HostRooms(APIView):

    def get(self, request, username):
        try:
            host = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        if not host.is_host:
            raise ParseError("The user does not own any rooms")
        rooms = host.rooms.all().order_by("-created_date")
        serializer = HostRoomSerializer(rooms, many=True)
        return Response(serializer.data)


class HostRoomReviews(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        host = self.get_object(username)
        if not host.is_host:
            raise ParseError("The User does not own any rooms")
        room_reviews = Review.objects.filter(room__host=host).order_by("room__pk")
        serializer = HostReviewSerializer(room_reviews, many=True)
        return Response(serializer.data)


class UserReviews(APIView):
    # see all reviews the user left

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User not found")

    def get(self, request, username):
        user = self.get_object(username)
        all_reviews = user.reviews.all().order_by("-created_date")
        serializer = UserReviewSerializer(all_reviews, many=True)
        return Response(serializer.data)


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)

        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        else:
            return Response({"Error": "Wrong Password"})
