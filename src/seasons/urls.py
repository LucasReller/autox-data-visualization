from django.urls import path

from . import views

app_name = "seasons"

urlpatterns = [
    path("", views.DriversView.as_view(), name="index"),
    path("<int:pk>", views.CompetitorView.as_view(), name="competitor"),
]