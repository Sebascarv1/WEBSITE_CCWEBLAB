from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.BookingHomeView.as_view(), name="home"),
    path("api/available-slots/", views.get_available_slots, name="api_available_slots"),
]