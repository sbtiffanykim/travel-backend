from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExperienceLists.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/includedItems", views.ExperienceItems.as_view()),
    # path("<int:pk>/reviews", views.ExperienceDetail.as_view()),
    # path("<int:pk>/bookings", views.ExperienceDetail.as_view()),
    # path("<int:pk>/photos", views.ExperienceDetail.as_view()),
    # path("<int:pk>/video", views.ExperienceDetail.as_view()),
    path("includedItems/", views.IncludedItems.as_view()),
    path("includedItems/<int:pk>", views.IncludedItemDetail.as_view()),
]
