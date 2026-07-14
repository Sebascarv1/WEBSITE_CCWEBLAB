# Gmail Email Configuration Setup

This guide explains how to configure email sending using Gmail instead of Hotmail.

## Overview

The booking system can send emails from any email provider. Gmail is a popular alternative to Hotmail.

## Gmail Setup Steps

### Option 1: Using App Passwords (Recommended)

**Requirements:**
- Gmail account (free or Google Workspace)
- 2-Step Verification enabled on your Google Account

#### Step 1: Enable 2-Step Verification

1. Go to https://myaccount.google.com
2. Click **Security** in the left sidebar
3. Scroll to **How you sign in to Google**
4. Click **2-Step Verification**
5. Follow the prompts to enable it

#### Step 2: Create App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select:
   - App: **Mail**
   - Device: **Windows Computer** (or your OS)
3. Click **Generate**
4. Copy the 16-character password shown

#### Step 3: Configure Environment Variables

Create a `.env` file in the project root with:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<your-16-char-app-password>
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_TO_EMAIL=admin@gairalabs.com
```

**Example:**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=bookings@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=bookings@gmail.com
CONTACT_TO_EMAIL=admin@gairalabs.com
```

### Option 2: Less Secure App Access (Deprecated - Not Recommended)

⚠️ **Google is deprecating this method. Use Option 1 instead.**

If you must use this:

1. Go to https://myaccount.google.com/lesssecureapps
2. Enable **Less secure app access**
3. Use your Gmail password (not app password)
4. Same environment variables as Option 1

**Note:** This will stop working soon.

---

## Production Deployment (Render)

### Step 1: Get Your Gmail Credentials

From Option 1 above, collect:
- `EMAIL_HOST_USER`: your-email@gmail.com
- `EMAIL_HOST_PASSWORD`: your 16-character app password (copy it exactly with spaces)

### Step 2: Add to Render

1. Go to https://dashboard.render.com
2. Select your **website-ccweblab** service
3. Click **Environment** tab
4. Click **Add Environment Variable** for each:

| Key | Value |
|-----|-------|
| EMAIL_HOST | smtp.gmail.com |
| EMAIL_PORT | 587 |
| EMAIL_USE_TLS | True |
| EMAIL_HOST_USER | your-email@gmail.com |
| EMAIL_HOST_PASSWORD | abcd efgh ijkl mnop |
| DEFAULT_FROM_EMAIL | your-email@gmail.com |
| CONTACT_TO_EMAIL | admin@gairalabs.com |

5. Click **Save**
6. Render will automatically redeploy with new settings

### Step 3: Test

Create a test booking on your site. You should receive confirmation emails within seconds.

---

## Comparing Email Providers

| Feature | Gmail | Hotmail | Google Workspace |
|---------|-------|---------|------------------|
| Free | ✅ Yes | ✅ Yes | ❌ $6-12/user/mo |
| Daily Limit | 500 emails | 1000 emails | Unlimited |
| Setup | Easy (2FA needed) | Easy | Professional |
| Professional | No (@gmail.com) | No (@hotmail.com) | ✅ Yes (custom domain) |
| Reliability | Excellent | Excellent | Excellent |

**Recommendation:**
- **Personal/Testing:** Gmail or Hotmail (free)
- **Production:** Google Workspace or custom domain (professional)

---

## Using a Professional Email Address

If you want `bookings@gairalabs.com`:

### Option A: Google Workspace (Recommended)

1. Sign up at https://workspace.google.com
2. Add your domain (gairalabs.com)
3. Create email: bookings@gairalabs.com
4. Use same setup as Gmail above

### Option B: Email Forwarding

1. Create `bookings@gairalabs.com` with your DNS provider
2. Forward to your personal Gmail: `your-email@gmail.com`
3. Use the forwarding Gmail for environment variables
4. Emails will appear to come from the professional address

---

## Troubleshooting Gmail

### "SMTP authentication failed"
- ✅ Use **App Password** (not account password)
- ✅ Copy exactly with spaces: `abcd efgh ijkl mnop`
- ✅ Don't use special characters
- ❌ Don't use your Gmail password

### "Less secure app access" error
- Enable 2-Step Verification first
- Use App Passwords instead

### Gmail blocking connection
- Ensure `EMAIL_USE_TLS=True`
- Use `EMAIL_PORT=587` (not 465)
- Some networks block SMTP ports - use a different network to test

### Emails going to spam
- Enable "Display name" in Django settings (optional)
- Verify sender email matches `EMAIL_HOST_USER`
- For professional domain, set up SPF/DKIM records

---

## Adding Display Name (Optional)

To show "Gaira Labs Bookings" instead of just email:

Update `settings.py`:

```python
DEFAULT_FROM_EMAIL = '"Gaira Labs Bookings" <bookings@gmail.com>'
```

Or via environment variable (if using dotenv):

```
DEFAULT_FROM_EMAIL="Gaira Labs Bookings <bookings@gmail.com>"
```

---

## Quick Comparison: Gmail vs Hotmail

**Gmail Setup:**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<16-char-app-password>
```

**Hotmail Setup:**
```
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@hotmail.com
EMAIL_HOST_PASSWORD=<16-char-app-password>
```

The only difference is the `EMAIL_HOST` and your email address.

---

## Testing Locally

Before deploying, test your Gmail config:

1. Create `.env` file with Gmail credentials
2. Run Django shell:

```bash
python ccweblab/manage.py shell
```

3. Test sending email:

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    subject='Test Email from Gmail',
    message='This is a test email',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['your-test-email@example.com'],
    fail_silently=False,
)
```

Expected output: `<Response [250]>` = Success ✅

---

## Still Need Help?

See the main `SETUP_EMAIL.md` for general email concepts, or check:
- Gmail Help: https://support.google.com/mail
- Django Email Docs: https://docs.djangoproject.com/en/6.0/topics/email/
