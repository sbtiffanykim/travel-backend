from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExperienceLists.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/inclusions", views.ExperienceItems.as_view()),
    # path("<int:pk>/reviews", views.ExperienceDetail.as_view()),
    # path("<int:pk>/bookings", views.ExperienceDetail.as_view()),
    # path("<int:pk>/photos", views.ExperienceDetail.as_view()),
    # path("<int:pk>/video", views.ExperienceDetail.as_view()),
    path("inclusions/", views.Inclusions.as_view()),
    path("inclusions/<int:pk>", views.InclusionDetail.as_view()),
]
