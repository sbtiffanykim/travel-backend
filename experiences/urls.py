from django.urls import path
from . import views

urlpatterns = [
    path("includeditems/", views.IncludedItems.as_view()),
    path("includeditems/<int:pk>", views.IncludedItemDetail.as_view()),
]
