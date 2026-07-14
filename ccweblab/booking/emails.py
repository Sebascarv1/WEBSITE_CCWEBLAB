"""Email notifications for bookings"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_booking_confirmation_email(booking):
    """Send confirmation email to customer after booking is created"""
    try:
        subject = f"Booking Confirmation — {booking.activity.name}"
        
        context = {
            "booking": booking,
            "activity_name": booking.activity.name,
            "customer_name": booking.full_name,
            "booking_date": booking.booking_date.strftime("%A, %B %d, %Y"),
            "booking_time": booking.booking_time.strftime("%I:%M %p"),
            "project_details": booking.project_details,
            "website_url": "https://gairalabs.com",
        }
        
        # Try to render HTML template, fall back to plain text
        try:
            html_message = render_to_string("booking/email_confirmation.html", context)
            plain_message = strip_tags(html_message)
        except:
            plain_message = f"""
Hello {booking.full_name},

Thank you for your booking!

Service: {booking.activity.name}
Date: {context['booking_date']}
Time: {context['booking_time']}

Your booking status is currently Pending. We will confirm your booking shortly.

If you have any questions, please contact us.

Best regards,
Gaira Labs Team
            """
            html_message = None
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending booking confirmation email: {e}")
        return False


def send_booking_admin_notification(booking):
    """Send notification email to admin about new booking"""
    try:
        subject = f"New Booking — {booking.activity.name} on {booking.booking_date}"
        
        context = {
            "booking": booking,
            "activity_name": booking.activity.name,
            "customer_name": booking.full_name,
            "customer_email": booking.email,
            "customer_phone": booking.phone,
            "booking_date": booking.booking_date.strftime("%A, %B %d, %Y"),
            "booking_time": booking.booking_time.strftime("%I:%M %p"),
            "project_details": booking.project_details,
            "budget": booking.budget or "Not specified",
            "timeline": booking.timeline or "Not specified",
            "admin_url": "https://gairalabs.com/admin/booking/booking/",
        }
        
        try:
            html_message = render_to_string("booking/email_admin_notification.html", context)
            plain_message = strip_tags(html_message)
        except:
            plain_message = f"""
New Booking Notification

Service: {booking.activity.name}
Customer: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}

Date: {context['booking_date']}
Time: {context['booking_time']}

Budget: {context['budget']}
Timeline: {context['timeline']}

Project Details:
{booking.project_details}

Status: {booking.get_status_display()}

Please review and confirm this booking in the admin dashboard.
            """
            html_message = None
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_TO_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending booking admin notification: {e}")
        return False


def send_booking_status_update(booking):
    """Send status update email to customer"""
    try:
        status_messages = {
            "pending": "Your booking is being reviewed",
            "confirmed": "Your booking has been confirmed!",
            "completed": "Thank you for your booking!",
            "cancelled": "Your booking has been cancelled",
        }
        
        subject = f"Booking Update — {booking.activity.name}"
        status_message = status_messages.get(booking.status, "Your booking has been updated")
        
        context = {
            "booking": booking,
            "activity_name": booking.activity.name,
            "customer_name": booking.full_name,
            "status_message": status_message,
            "booking_date": booking.booking_date.strftime("%A, %B %d, %Y"),
            "booking_time": booking.booking_time.strftime("%I:%M %p"),
        }
        
        try:
            html_message = render_to_string("booking/email_status_update.html", context)
            plain_message = strip_tags(html_message)
        except:
            plain_message = f"""
Hello {booking.full_name},

{status_message}

Service: {booking.activity.name}
Date: {context['booking_date']}
Time: {context['booking_time']}

Booking Status: {booking.get_status_display()}

Best regards,
Gaira Labs Team
            """
            html_message = None
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending status update email: {e}")
        return False
