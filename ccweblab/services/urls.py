# services/urls.py
from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("contact/", views.contact, name="contact"),
]