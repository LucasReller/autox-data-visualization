from django.urls import path

from . import views

app_name = "seasons"

urlpatterns = [
    path("", views.DriversListView.as_view(), name="index"),
    path("driver/<int:pk>/", views.DriverView.as_view(), name="driver"),
    path("<int:pk>", views.CompetitorView.as_view(), name="competitor"),

]