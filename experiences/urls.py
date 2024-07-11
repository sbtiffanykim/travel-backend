from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExperienceList.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/inclusions", views.ExperienceItems.as_view()),
    path("<int:pk>/reviews", views.ExperienceReviews.as_view()),
    path("<int:pk>/photos", views.ExperiencePhotos.as_view()),
    path("<int:pk>/video", views.ExperienceVideo.as_view()),
    # path("<int:pk>/bookings", views.ExperienceDetail.as_view()),
    path("inclusions/", views.InclusionList.as_view()),
    path("inclusions/<int:pk>", views.InclusionDetail.as_view()),
]
