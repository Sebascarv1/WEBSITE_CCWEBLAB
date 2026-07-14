from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.BookingHomeView.as_view(), name="home"),
    path("api/available-slots/", views.get_available_slots, name="api_available_slots"),
    path("management/", views.booking_management, name="management"),
    path("api/update-status/", views.update_booking_status, name="update_status"),
    path("admin/add-activity/", views.add_activity, name="add_activity"),
    path("admin/add-availability-slot/", views.add_availability_slot, name="add_availability_slot"),
]