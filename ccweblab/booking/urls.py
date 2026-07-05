from django.urls import path
from .views import BookingHomeView

app_name = "booking"

urlpatterns = [
    path("", BookingHomeView.as_view(), name="home"),
]