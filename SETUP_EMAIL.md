# Email Configuration Setup

This guide explains how to configure email sending for booking confirmations using a Hotmail/Outlook account.

## Overview

When a booking is made on the system:
1. **Customer Email**: Confirmation email is sent to the customer with booking details
2. **Admin Email**: Notification email is sent to the admin/business contact
3. **Status Updates**: When booking status changes, the customer is notified via email

## Email Configuration Steps

### 1. Set Up Hotmail/Outlook Account

If you don't have a Hotmail account yet:
- Create a free account at https://outlook.live.com
- For this example: `test@hotmail.com`

### 2. Create an App Password

Outlook/Hotmail requires an "App Password" for email client access (for security):

1. Go to https://account.microsoft.com/account/manage-my-microsoft-account
2. Click **Security** in the left sidebar
3. Under **Advanced security options**, click **App passwords**
4. Select:
   - App: **Mail**
   - Device: **Other (custom)** → type "Django"
5. Click **Create**
6. Copy the generated 16-character password

### 3. Configure Environment Variables

Create a `.env` file in the project root with:

```
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=test@hotmail.com
EMAIL_HOST_PASSWORD=<your-16-char-app-password>
DEFAULT_FROM_EMAIL=test@hotmail.com
CONTACT_TO_EMAIL=admin@gairalabs.com
```

**Important:**
- Replace `test@hotmail.com` with your actual email
- Replace `<your-16-char-app-password>` with the password from step 2 (without spaces)
- Replace `admin@gairalabs.com` with your business contact email

### 4. Django Settings Already Configured

The `settings.py` file is already set up to read these environment variables:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp-mail.outlook.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "test@hotmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "test@hotmail.com")
```

No code changes needed!

## Testing Email Configuration

### Local Development

To test emails locally, run:

```bash
python ccweblab/manage.py shell
```

Then paste:

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Test Email',
    message='This is a test email from Django',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-test-email@example.com'],
    fail_silently=False,
)
```

If successful, you'll see `<Response [250]>` and receive the email.

### Production (Render)

1. Go to your Render deployment dashboard
2. Navigate to **Environment** → **Environment Variables**
3. Add all the email configuration variables:
   - `EMAIL_HOST`
   - `EMAIL_PORT`
   - `EMAIL_USE_TLS`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `DEFAULT_FROM_EMAIL`
   - `CONTACT_TO_EMAIL`
4. Redeploy the application

## Email Templates

Email templates are located in:
- `templates/booking/email_confirmation.html` - Customer confirmation
- `templates/booking/email_admin_notification.html` - Admin notification
- `templates/booking/email_status_update.html` - Status change notification

Each template is HTML-formatted and falls back to plain text if rendering fails.

## Email Sending Flow

### When Booking is Created

```
BookingHomeView.post()
├── Create Booking object
├── send_booking_confirmation_email(booking)  ← Customer email
└── send_booking_admin_notification(booking)  ← Admin email
```

### When Status is Updated

```
update_booking_status()
├── Update booking.status
└── send_booking_status_update(booking)  ← Customer email
```

## Troubleshooting

### "SMTP authentication failed"
- Verify app password is correct (no spaces)
- Make sure you used an **App Password**, not your account password
- Verify `EMAIL_HOST_USER` matches the email account

### "Connection refused on port 587"
- Check firewall/network allows outbound SMTP
- Verify `EMAIL_PORT=587` and `EMAIL_USE_TLS=True`

### "Emails not sending but no errors"
- Check that `fail_silently=False` in `emails.py` for debugging
- Check Django logs for error messages
- Verify `DEFAULT_FROM_EMAIL` is a valid email address

### "Email looks like spam"
- Ensure `DEFAULT_FROM_EMAIL` matches the authenticated email account
- Use a professional email domain if available (not @hotmail.com)
- Avoid common spam trigger words

## Using a Custom Domain Email

If you want to use `bookings@gairalabs.com`:

1. Set up email forwarding on your domain registrar/DNS
2. Or use a professional email service like:
   - Gmail (Google Workspace)
   - Microsoft 365
   - Zoho Mail
   - Proton Mail

Then update the environment variables accordingly.

## Gmail Alternative (Less Secure Method)

If you prefer Gmail:

1. Enable "Less secure app access" in Google Account settings
2. Use `EMAIL_HOST=smtp.gmail.com`
3. Use your Gmail password (or app password)

**Note**: Gmail's "Less secure app access" is deprecated. Use app passwords instead.

---

**For support:** Contact your web administrator or check Django email documentation at https://docs.djangoproject.com/en/6.0/topics/email/
