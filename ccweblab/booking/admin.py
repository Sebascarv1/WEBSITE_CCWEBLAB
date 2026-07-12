from django.contrib import admin
from .models import Activity, AvailabilitySlot, Booking, BookingTerms


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_minutes", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    fieldsets = (
        ("Activity Info", {"fields": ("name", "description")}),
        ("Settings", {"fields": ("duration_minutes", "is_active")}),
    )


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ["activity", "day_of_week", "start_time", "end_time", "max_bookings_per_slot", "is_active"]
    list_filter = ["activity", "day_of_week", "is_active"]
    fieldsets = (
        ("Slot Info", {"fields": ("activity", "day_of_week", "start_time", "end_time")}),
        ("Settings", {"fields": ("max_bookings_per_slot", "is_active")}),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["full_name", "activity", "booking_date", "booking_time", "status", "created_at"]
    list_filter = ["status", "booking_date", "activity", "created_at"]
    search_fields = ["full_name", "email", "phone"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Customer Info", {"fields": ("full_name", "email", "phone")}),
        ("Booking Info", {"fields": ("activity", "booking_date", "booking_time")}),
        ("Details", {"fields": ("project_details", "budget", "timeline")}),
        ("Status", {"fields": ("status", "terms_accepted")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ["full_name", "email", "activity", "booking_date", "booking_time"]
        return self.readonly_fields


@admin.register(BookingTerms)
class BookingTermsAdmin(admin.ModelAdmin):
    list_display = ["title", "version", "is_active", "updated_at"]
    list_filter = ["is_active", "version"]
    fieldsets = (
        ("Terms Info", {"fields": ("title", "version", "is_active")}),
        ("Content", {"fields": ("content",)}),
    )
