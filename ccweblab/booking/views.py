from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
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


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def booking_management(request):
    """Admin-only booking management dashboard"""
    template_name = "booking/management.html"
    
    # Get filter parameters
    status = request.GET.get("status", "")
    activity_id = request.GET.get("activity", "")
    sort_by = request.GET.get("sort", "-created_at")
    search = request.GET.get("search", "")
    
    # Base queryset
    bookings = Booking.objects.all()
    
    # Apply filters
    if status:
        bookings = bookings.filter(status=status)
    
    if activity_id:
        bookings = bookings.filter(activity_id=activity_id)
    
    if search:
        bookings = bookings.filter(full_name__icontains=search) | bookings.filter(email__icontains=search)
    
    # Sort
    valid_sorts = ["-created_at", "created_at", "booking_date", "-booking_date", "full_name"]
    if sort_by not in valid_sorts:
        sort_by = "-created_at"
    bookings = bookings.order_by(sort_by)
    
    # Get stats
    total_bookings = Booking.objects.count()
    pending_count = Booking.objects.filter(status="pending").count()
    confirmed_count = Booking.objects.filter(status="confirmed").count()
    completed_count = Booking.objects.filter(status="completed").count()
    cancelled_count = Booking.objects.filter(status="cancelled").count()
    
    context = {
        "bookings": bookings,
        "activities": Activity.objects.filter(is_active=True),
        "status_choices": Booking.STATUS_CHOICES,
        "stats": {
            "total": total_bookings,
            "pending": pending_count,
            "confirmed": confirmed_count,
            "completed": completed_count,
            "cancelled": cancelled_count,
        },
        "current_status": status,
        "current_activity": activity_id,
        "current_sort": sort_by,
        "search_term": search,
    }
    
    return render(request, template_name, context)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
@require_http_methods(["POST"])
def update_booking_status(request):
    """Update booking status via AJAX"""
    try:
        booking_id = request.POST.get("booking_id")
        new_status = request.POST.get("status")
        
        if new_status not in dict(Booking.STATUS_CHOICES):
            return JsonResponse({"error": "Invalid status"}, status=400)
        
        booking = Booking.objects.get(id=booking_id)
        old_status = booking.status
        booking.status = new_status
        booking.save()
        
        return JsonResponse({
            "success": True,
            "booking_id": booking_id,
            "old_status": old_status,
            "new_status": new_status,
        })
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def add_activity(request):
    """Add a new activity/service"""
    template_name = "booking/add_activity.html"
    
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            duration_minutes = request.POST.get("duration_minutes", "30")
            is_active = request.POST.get("is_active") == "on"
            
            # Validation
            if not name:
                return render(request, template_name, {"error": "Activity name is required"})
            
            if Activity.objects.filter(name__iexact=name).exists():
                return render(request, template_name, {"error": "Activity with this name already exists"})
            
            try:
                duration = int(duration_minutes)
                if duration < 15 or duration > 480:
                    raise ValueError("Duration must be between 15 and 480 minutes")
            except ValueError:
                return render(request, template_name, {"error": "Invalid duration"})
            
            # Create activity
            activity = Activity.objects.create(
                name=name,
                description=description,
                duration_minutes=duration,
                is_active=is_active,
            )
            
            return render(request, template_name, {
                "success": f"Activity '{activity.name}' created successfully!",
                "activity": activity,
            })
        
        except Exception as e:
            return render(request, template_name, {"error": f"Error: {str(e)}"})
    
    context = {
        "activities": Activity.objects.all().order_by("-created_at"),
    }
    return render(request, template_name, context)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def add_availability_slot(request):
    """Add availability slots for an activity"""
    template_name = "booking/add_availability_slot.html"
    
    if request.method == "POST":
        try:
            activity_id = request.POST.get("activity")
            day_of_week = request.POST.get("day_of_week")
            start_time_str = request.POST.get("start_time")
            end_time_str = request.POST.get("end_time")
            max_bookings = request.POST.get("max_bookings_per_slot", "1")
            is_active = request.POST.get("is_active") == "on"
            
            # Validation
            if not all([activity_id, day_of_week, start_time_str, end_time_str]):
                return render(request, template_name, {
                    "error": "All fields are required",
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            try:
                activity = Activity.objects.get(id=activity_id)
                day_of_week = int(day_of_week)
                start_time = datetime.strptime(start_time_str, "%H:%M").time()
                end_time = datetime.strptime(end_time_str, "%H:%M").time()
                max_bookings = int(max_bookings)
                
                if max_bookings < 1 or max_bookings > 100:
                    raise ValueError("Max bookings must be between 1 and 100")
                
                if start_time >= end_time:
                    raise ValueError("Start time must be before end time")
                
            except (ValueError, Activity.DoesNotExist) as e:
                return render(request, template_name, {
                    "error": f"Invalid input: {str(e)}",
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            # Check if slot already exists
            if AvailabilitySlot.objects.filter(
                activity=activity,
                day_of_week=day_of_week,
                start_time=start_time,
            ).exists():
                return render(request, template_name, {
                    "error": "This slot already exists for this activity and day",
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            # Create slot
            slot = AvailabilitySlot.objects.create(
                activity=activity,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time,
                max_bookings_per_slot=max_bookings,
                is_active=is_active,
            )
            
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_name = day_names[int(day_of_week)]
            
            return render(request, template_name, {
                "success": f"Availability slot for {activity.name} on {day_name} created successfully!",
                "activities": Activity.objects.filter(is_active=True),
                "slots": AvailabilitySlot.objects.filter(activity__is_active=True).select_related("activity").order_by("activity", "day_of_week", "start_time"),
            })
        
        except Exception as e:
            return render(request, template_name, {
                "error": f"Error: {str(e)}",
                "activities": Activity.objects.filter(is_active=True),
            })
    
    context = {
        "activities": Activity.objects.filter(is_active=True),
        "days_of_week": AvailabilitySlot.DAYS_OF_WEEK,
        "slots": AvailabilitySlot.objects.select_related("activity").order_by("activity", "day_of_week", "start_time"),
    }
    return render(request, template_name, context)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def edit_activity(request, activity_id):
    """Edit an existing activity"""
    template_name = "booking/edit_activity.html"
    
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return redirect("booking:add_activity")
    
    if request.method == "POST":
        try:
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            duration_minutes = request.POST.get("duration_minutes", "30")
            is_active = request.POST.get("is_active") == "on"
            
            if not name:
                return render(request, template_name, {"error": "Activity name is required", "activity": activity})
            
            if name != activity.name and Activity.objects.filter(name__iexact=name).exists():
                return render(request, template_name, {"error": "Activity with this name already exists", "activity": activity})
            
            try:
                duration = int(duration_minutes)
                if duration < 15 or duration > 480:
                    raise ValueError("Duration must be between 15 and 480 minutes")
            except ValueError:
                return render(request, template_name, {"error": "Invalid duration", "activity": activity})
            
            activity.name = name
            activity.description = description
            activity.duration_minutes = duration
            activity.is_active = is_active
            activity.save()
            
            return render(request, template_name, {
                "success": f"Activity '{activity.name}' updated successfully!",
                "activity": activity,
            })
        
        except Exception as e:
            return render(request, template_name, {"error": f"Error: {str(e)}", "activity": activity})
    
    context = {"activity": activity}
    return render(request, template_name, context)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
@require_http_methods(["POST"])
def delete_activity(request, activity_id):
    """Delete an activity"""
    try:
        activity = Activity.objects.get(id=activity_id)
        activity_name = activity.name
        activity.delete()
        return JsonResponse({"success": True, "message": f"Activity '{activity_name}' deleted successfully"})
    except Activity.DoesNotExist:
        return JsonResponse({"error": "Activity not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def edit_availability_slot(request, slot_id):
    """Edit an existing availability slot"""
    template_name = "booking/edit_availability_slot.html"
    
    try:
        slot = AvailabilitySlot.objects.select_related("activity").get(id=slot_id)
    except AvailabilitySlot.DoesNotExist:
        return redirect("booking:add_availability_slot")
    
    if request.method == "POST":
        try:
            activity_id = request.POST.get("activity")
            day_of_week = request.POST.get("day_of_week")
            start_time_str = request.POST.get("start_time")
            end_time_str = request.POST.get("end_time")
            max_bookings = request.POST.get("max_bookings_per_slot", "1")
            is_active = request.POST.get("is_active") == "on"
            
            if not all([activity_id, day_of_week, start_time_str, end_time_str]):
                return render(request, template_name, {
                    "error": "All fields are required",
                    "slot": slot,
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            try:
                activity = Activity.objects.get(id=activity_id)
                day_of_week = int(day_of_week)
                start_time = datetime.strptime(start_time_str, "%H:%M").time()
                end_time = datetime.strptime(end_time_str, "%H:%M").time()
                max_bookings = int(max_bookings)
                
                if max_bookings < 1 or max_bookings > 100:
                    raise ValueError("Max bookings must be between 1 and 100")
                
                if start_time >= end_time:
                    raise ValueError("Start time must be before end time")
                
            except (ValueError, Activity.DoesNotExist) as e:
                return render(request, template_name, {
                    "error": f"Invalid input: {str(e)}",
                    "slot": slot,
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            # Check if duplicate exists (excluding current slot)
            if AvailabilitySlot.objects.filter(
                activity=activity,
                day_of_week=day_of_week,
                start_time=start_time,
            ).exclude(id=slot_id).exists():
                return render(request, template_name, {
                    "error": "This slot already exists for this activity and day",
                    "slot": slot,
                    "activities": Activity.objects.filter(is_active=True),
                })
            
            slot.activity = activity
            slot.day_of_week = day_of_week
            slot.start_time = start_time
            slot.end_time = end_time
            slot.max_bookings_per_slot = max_bookings
            slot.is_active = is_active
            slot.save()
            
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day_name = day_names[int(day_of_week)]
            
            return render(request, template_name, {
                "success": f"Availability slot for {activity.name} on {day_name} updated successfully!",
                "slot": slot,
                "activities": Activity.objects.filter(is_active=True),
            })
        
        except Exception as e:
            return render(request, template_name, {
                "error": f"Error: {str(e)}",
                "slot": slot,
                "activities": Activity.objects.filter(is_active=True),
            })
    
    context = {
        "slot": slot,
        "activities": Activity.objects.filter(is_active=True),
        "days_of_week": AvailabilitySlot.DAYS_OF_WEEK,
    }
    return render(request, template_name, context)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
@require_http_methods(["POST"])
def delete_availability_slot(request, slot_id):
    """Delete an availability slot"""
    try:
        slot = AvailabilitySlot.objects.select_related("activity").get(id=slot_id)
        activity_name = slot.activity.name
        slot.delete()
        return JsonResponse({"success": True, "message": f"Slot deleted successfully"})
    except AvailabilitySlot.DoesNotExist:
        return JsonResponse({"error": "Slot not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url="admin:login")
@user_passes_test(is_admin, login_url="admin:login")
def booking_agenda(request):
    """Calendar/agenda view of bookings"""
    template_name = "booking/agenda.html"
    
    # Get date from request or use today
    date_str = request.GET.get("date")
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    day_of_week = selected_date.weekday()
    
    # Get all activities
    activities = Activity.objects.filter(is_active=True)
    
    # Get slots for this day
    slots = AvailabilitySlot.objects.filter(
        day_of_week=day_of_week,
        is_active=True
    ).select_related("activity").order_by("start_time")
    
    # Build agenda data
    agenda = {}
    for slot in slots:
        if slot.activity.id not in agenda:
            agenda[slot.activity.id] = {
                "activity": slot.activity,
                "slots": []
            }
        
        # Get bookings for this slot
        bookings = Booking.objects.filter(
            activity=slot.activity,
            booking_date=selected_date,
            booking_time=slot.start_time,
        ).order_by("created_at")
        
        slot_data = {
            "slot": slot,
            "bookings": list(bookings),
            "available_spots": slot.max_bookings_per_slot - bookings.count(),
            "is_full": bookings.count() >= slot.max_bookings_per_slot,
        }
        agenda[slot.activity.id]["slots"].append(slot_data)
    
    # Date navigation
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = day_names[day_of_week]
    
    context = {
        "selected_date": selected_date,
        "day_name": day_name,
        "prev_date": prev_date,
        "next_date": next_date,
        "agenda": agenda.values(),
        "activities": activities,
    }
    return render(request, template_name, context)