from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render


def welcome(request):
    # Renders your landing page with the form.
    return render(request, "services/welcome.html")


def contact(request):
    """
    Handles POST from the "Get a quote" form.
    - Validates required fields
    - Sends an email to CONTACT_TO_EMAIL (or DEFAULT_FROM_EMAIL as fallback)
    - Redirects back to the welcome page with a success/error message
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    service = (request.POST.get("service") or "").strip()
    budget = (request.POST.get("budget") or "").strip()
    user_message = (request.POST.get("message") or "").strip()

    # Basic validation
    if not name or not email or not user_message:
        messages.error(request, "Please fill in your name, email, and project details.")
        return redirect("services:welcome")

    subject = f"New Quote Request — {name} ({service or 'General'})"
    body = (
        f"New quote request received.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Service: {service}\n"
        f"Budget: {budget}\n\n"
        f"Message:\n{user_message}\n"
    )

    to_email = getattr(settings, "CONTACT_TO_EMAIL", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or to_email

    if not to_email or not from_email:
        messages.error(
            request,
            "Server email is not configured yet. Set CONTACT_TO_EMAIL and DEFAULT_FROM_EMAIL in settings.py.",
        )
        return redirect("services:welcome")

    try:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=[to_email],
            reply_to=[email],  # Reply to the user when you click "Reply" in your inbox
        )
        msg.send(fail_silently=False)
    except Exception:
        # Optional: you can log the exception here
        messages.error(request, "Sorry—your message could not be sent right now. Please try again later.")
        return redirect("services:welcome")

    messages.success(request, "Thanks! Your message was sent. We’ll reply soon.")
    return redirect("services:welcome")