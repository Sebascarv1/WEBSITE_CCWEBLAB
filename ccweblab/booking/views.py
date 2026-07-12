from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Activity, AvailabilitySlot, Booking, BookingTerms


class BookingHomeView(View):
    """Main booking form page"""
    template_name = "booking/home.html"

    def get(self, request, *args, **kwargs):
        context = {
            "activities": Activity.objects.filter(is_active=True),
            "terms": BookingTerms.objects.filter(is_active=True).first(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle booking form submission"""
        try:
            activity_id = request.POST.get("activity")
            booking_date_str = request.POST.get("booking_date")
            booking_time_str = request.POST.get("booking_time")
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone", "")
            budget = request.POST.get("budget", "")
            timeline = request.POST.get("timeline", "")
            project_details = request.POST.get("project_details")
            terms_accepted = request.POST.get("terms_accepted") == "on"

            # Validation
            if not all([activity_id, booking_date_str, booking_time_str, full_name, email, project_details]):
                return render(
                    request,
                    self.template_name,
                    {"error": "All required fields must be filled.", "activities": Activity.objects.filter(is_active=True)},
                )

            if not terms_accepted:
                return render(
                    request,
                    self.template_name,
                    {"error": "You must accept the terms and conditions.", "activities": Activity.objects.filter(is_active=True)},
                )

            activity = Activity.objects.get(id=activity_id)
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
            booking_time = datetime.strptime(booking_time_str, "%H:%M").time()

            # Check if slot is still available
            booking_count = Booking.objects.filter(
                activity=activity,
                booking_date=booking_date,
                booking_time=booking_time,
                status__in=["pending", "confirmed"],
            ).count()

            # Get the slot
            day_of_week = booking_date.weekday()
            slot = AvailabilitySlot.objects.filter(
                activity=activity,
                day_of_week=day_of_week,
                start_time__lte=booking_time,
                is_active=True,
            ).first()

            if not slot or booking_count >= slot.max_bookings_per_slot:
                return render(
                    request,
                    self.template_name,
                    {"error": "This time slot is no longer available.", "activities": Activity.objects.filter(is_active=True)},
                )

            # Create booking
            booking = Booking.objects.create(
                activity=activity,
                full_name=full_name,
                email=email,
                phone=phone,
                booking_date=booking_date,
                booking_time=booking_time,
                budget=budget,
                timeline=timeline,
                project_details=project_details,
                terms_accepted=terms_accepted,
                status="pending",
            )

            return render(
                request,
                "booking/confirmation.html",
                {"booking": booking, "success": True},
            )

        except Activity.DoesNotExist:
            return render(request, self.template_name, {"error": "Invalid activity selected."})
        except Exception as e:
            return render(
                request,
                self.template_name,
                {"error": f"An error occurred: {str(e)}", "activities": Activity.objects.filter(is_active=True)},
            )


@require_http_methods(["GET"])
def get_available_slots(request):
    """API endpoint to get available slots for an activity and date"""
    activity_id = request.GET.get("activity_id")
    date_str = request.GET.get("date")

    if not activity_id or not date_str:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        activity = Activity.objects.get(id=activity_id, is_active=True)
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        day_of_week = booking_date.weekday()

        # Get available slots for this day and activity
        slots = AvailabilitySlot.objects.filter(
            activity=activity,
            day_of_week=day_of_week,
            is_active=True,
        ).order_by("start_time")

        if not slots.exists():
            return JsonResponse({"slots": [], "message": "No slots available for this date"})

        available_slots = []
        for slot in slots:
            # Count existing bookings for this time
            booking_count = Booking.objects.filter(
                activity=activity,
                booking_date=booking_date,
                booking_time=slot.start_time,
                status__in=["pending", "confirmed"],
            ).count()

            availability = max(0, slot.max_bookings_per_slot - booking_count)

            available_slots.append(
                {
                    "time": slot.start_time.strftime("%H:%M"),
                    "available": availability > 0,
                    "spots_left": availability,
                }
            )

        return JsonResponse({"slots": available_slots})

    except Activity.DoesNotExist:
        return JsonResponse({"error": "Activity not found"}, status=404)
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)