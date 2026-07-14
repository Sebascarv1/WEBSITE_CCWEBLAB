"""Email notifications for bookings"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from threading import Thread
import logging

logger = logging.getLogger(__name__)


def _send_booking_confirmation_email_async(booking):
    """Internal function to send confirmation email in background thread"""
    logger.info(f"[EMAIL] Starting confirmation email send for booking {booking.id}")
    try:
        subject = f"Booking Confirmation — {booking.activity.name}"
        logger.debug(f"[EMAIL] Confirmation email subject: {subject}")
        logger.debug(f"[EMAIL] Recipient: {booking.email}")
        
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
            logger.debug("[EMAIL] Using HTML template for confirmation email")
        except Exception as template_error:
            logger.warning(f"[EMAIL] Failed to render HTML template: {template_error}. Using plain text.")
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
        
        logger.info(f"[EMAIL] Sending confirmation email to {booking.email} via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"[EMAIL] ✓ Booking confirmation email successfully sent to {booking.email} for booking {booking.id}")
    except Exception as e:
        logger.error(f"[EMAIL] ✗ Error sending booking confirmation email for booking {booking.id}: {type(e).__name__}: {e}", exc_info=True)


def send_booking_confirmation_email(booking):
    """Send confirmation email to customer (non-blocking)"""
    logger.debug(f"[EMAIL] Spawning background thread for confirmation email (booking {booking.id})")
    thread = Thread(target=_send_booking_confirmation_email_async, args=(booking,), daemon=True)
    thread.start()
    logger.debug(f"[EMAIL] Background thread started for confirmation email")


def _send_booking_admin_notification_async(booking):
    """Internal function to send admin notification in background thread"""
    logger.info(f"[EMAIL] Starting admin notification send for booking {booking.id}")
    try:
        subject = f"New Booking — {booking.activity.name} on {booking.booking_date}"
        logger.debug(f"[EMAIL] Admin notification subject: {subject}")
        logger.debug(f"[EMAIL] Admin recipient: {settings.CONTACT_TO_EMAIL}")
        
        context = {
            "booking": booking,
            "activity_name": booking.activity.name,
            "customer_name": booking.full_name,
            "customer_email": booking.email,
            "customer_phone": booking.phone,
        }
        
        try:
            html_message = render_to_string("booking/email_admin_notification.html", context)
            plain_message = strip_tags(html_message)
            logger.debug("[EMAIL] Using HTML template for admin notification")
        except Exception as template_error:
            logger.warning(f"[EMAIL] Failed to render HTML template: {template_error}. Using plain text.")
            plain_message = f"""
New Booking Received

Service: {booking.activity.name}
Customer: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}
Date: {booking.booking_date}
Time: {booking.booking_time}
Status: {booking.status}
            """
            html_message = None
        
        logger.info(f"[EMAIL] Sending admin notification to {settings.CONTACT_TO_EMAIL} via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_TO_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"[EMAIL] ✓ Admin notification successfully sent for booking {booking.id}")
    except Exception as e:
        logger.error(f"[EMAIL] ✗ Error sending admin notification for booking {booking.id}: {type(e).__name__}: {e}", exc_info=True)


def send_booking_admin_notification(booking):
    """Send notification email to admin (non-blocking)"""
    logger.debug(f"[EMAIL] Spawning background thread for admin notification (booking {booking.id})")
    thread = Thread(target=_send_booking_admin_notification_async, args=(booking,), daemon=True)
    thread.start()
    logger.debug(f"[EMAIL] Background thread started for admin notification")


def _send_booking_status_update_async(booking):
    """Internal function to send status update in background thread"""
    logger.info(f"[EMAIL] Starting status update email send for booking {booking.id}")
    try:
        status_messages = {
            "pending": "Your booking is being reviewed",
            "confirmed": "Your booking has been confirmed!",
            "completed": "Thank you for your booking!",
            "cancelled": "Your booking has been cancelled",
        }
        
        subject = f"Booking Update — {booking.activity.name}"
        status_message = status_messages.get(booking.status, "Your booking has been updated")
        logger.debug(f"[EMAIL] Status update subject: {subject}")
        logger.debug(f"[EMAIL] Status message: {status_message}")
        logger.debug(f"[EMAIL] Recipient: {booking.email}")
        
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
            logger.debug("[EMAIL] Using HTML template for status update email")
        except Exception as template_error:
            logger.warning(f"[EMAIL] Failed to render HTML template: {template_error}. Using plain text.")
            plain_message = f"""
Hello {booking.full_name},

{status_message}

Service: {booking.activity.name}
Date: {context['booking_date']}
Time: {context['booking_time']}

Booking Status: {booking.get_status_display()}

If you have any questions, please contact us.

Best regards,
Gaira Labs Team
            """
            html_message = None
        
        logger.info(f"[EMAIL] Sending status update email to {booking.email} via {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"[EMAIL] ✓ Status update email successfully sent to {booking.email} for booking {booking.id}")
    except Exception as e:
        logger.error(f"[EMAIL] ✗ Error sending status update email for booking {booking.id}: {type(e).__name__}: {e}", exc_info=True)


def send_booking_status_update(booking):
    """Send status update email to customer (non-blocking)"""
    logger.debug(f"[EMAIL] Spawning background thread for status update email (booking {booking.id})")
    thread = Thread(target=_send_booking_status_update_async, args=(booking,), daemon=True)
    thread.start()
    logger.debug(f"[EMAIL] Background thread started for status update email")
