from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [
    path("", views.CreateAccount.as_view()),
    path("me", views.PrivateUserProfile.as_view()),
    path("@<str:username>", views.PublicUserProfile.as_view()),
    path("@<str:username>/rooms", views.HostRooms.as_view()),
    path("@<str:username>/rooms/reviews", views.HostRoomReviews.as_view()),
    path("@<str:username>/reviews", views.UserReviews.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("get-token", obtain_auth_token),
]
