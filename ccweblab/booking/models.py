from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Activity(models.Model):
    """Service/Activity types available for booking"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AvailabilitySlot(models.Model):
    """Define available time slots for each activity"""
    DAYS_OF_WEEK = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="slots")
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_bookings_per_slot = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["activity", "day_of_week", "start_time"]
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.activity.name} - {self.get_day_of_week_display()} {self.start_time}"


class Booking(models.Model):
    """Customer booking records"""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    budget = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    project_details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "booking_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.activity} ({self.booking_date})"


class BookingTerms(models.Model):
    """Terms and conditions for bookings"""
    title = models.CharField(max_length=200, default="Booking Terms & Conditions")
    content = models.TextField()
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Booking Terms"
        ordering = ["-version"]

    def __str__(self):
        return f"{self.title} (v{self.version})"
