from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.BookingHomeView.as_view(), name="home"),
    path("api/available-slots/", views.get_available_slots, name="api_available_slots"),
    path("management/", views.booking_management, name="management"),
    path("agenda/", views.booking_agenda, name="agenda"),
    path("api/update-status/", views.update_booking_status, name="update_status"),
    path("admin/add-activity/", views.add_activity, name="add_activity"),
    path("admin/edit-activity/<int:activity_id>/", views.edit_activity, name="edit_activity"),
    path("admin/delete-activity/<int:activity_id>/", views.delete_activity, name="delete_activity"),
    path("admin/add-availability-slot/", views.add_availability_slot, name="add_availability_slot"),
    path("admin/edit-availability-slot/<int:slot_id>/", views.edit_availability_slot, name="edit_availability_slot"),
    path("admin/delete-availability-slot/<int:slot_id>/", views.delete_availability_slot, name="delete_availability_slot"),
]