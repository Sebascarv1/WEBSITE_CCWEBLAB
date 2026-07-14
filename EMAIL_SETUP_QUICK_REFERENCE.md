# Email Setup Quick Reference

## 📧 Supported Email Providers

### Gmail ✅ Recommended
- **Cost:** Free
- **Setup Time:** ~5 minutes
- **Daily Limit:** 500 emails
- **Best For:** Testing, small projects, personal use

### Hotmail/Outlook ✅ Good
- **Cost:** Free
- **Setup Time:** ~5 minutes
- **Daily Limit:** 1000 emails
- **Best For:** Testing, backup option

### Google Workspace ✅ Professional
- **Cost:** $6-12/user/month
- **Setup Time:** ~10 minutes
- **Daily Limit:** Unlimited
- **Best For:** Production, professional domain (bookings@gairalabs.com)

---

## 🚀 Quick Start: Gmail

### Step 1: Enable 2-Step Verification (2 minutes)
```
1. Go to https://myaccount.google.com
2. Click "Security" → "2-Step Verification"
3. Complete the setup
```

### Step 2: Get App Password (1 minute)
```
1. Go to https://myaccount.google.com/apppasswords
2. Select: Mail + Windows Computer
3. Click Generate
4. Copy the 16-character password
```

### Step 3: Update Environment Variables (2 minutes)

**Local Development (.env file):**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_TO_EMAIL=admin@gairalabs.com
```

**Production (Render Dashboard):**
1. Go to dashboard.render.com → Your Service
2. Click "Environment"
3. Add each variable above
4. Click "Save" (auto-redeploy)

### ✅ Done! Test with a booking

---

## 🔄 Side-by-Side Comparison

| Task | Gmail | Hotmail | Workspace |
|------|-------|---------|-----------|
| Create Account | [gmail.com](https://mail.google.com) | [outlook.com](https://outlook.live.com) | [workspace.google.com](https://workspace.google.com) |
| Enable 2FA | Settings → Security | Account → Advanced Security | Built-in |
| App Password | myaccount.google.com/apppasswords | account.microsoft.com/apppasswords | Same as Gmail |
| SMTP Host | smtp.gmail.com | smtp-mail.outlook.com | smtp.gmail.com |
| SMTP Port | 587 | 587 | 587 |
| TLS | True | True | True |
| Setup Difficulty | ⭐ Easy | ⭐ Easy | ⭐⭐ Medium |

---

## ❓ FAQ

### Q: Should I use Gmail or Hotmail?
**A:** Both work equally well. Choose whichever you prefer:
- Gmail: Better integration with Google ecosystem
- Hotmail: Better integration with Microsoft ecosystem
- Either works fine for booking emails

### Q: Can I use my regular Gmail password?
**A:** ❌ No. You MUST use an App Password for security:
1. Gmail won't allow direct SMTP access with regular password
2. App passwords are safer and can be revoked
3. Takes 1 minute to create

### Q: I get "authentication failed" error
**A:** Check these:
- [ ] Are you using an **App Password** (not regular password)?
- [ ] Did you copy it exactly with spaces? (`abcd efgh ijkl mnop`)
- [ ] Did you enable 2-Step Verification first?
- [ ] Is `EMAIL_HOST_USER` exactly your email address?

### Q: How many emails can I send per day?
**A:** 
- Gmail: 500 emails/day
- Hotmail: 1000 emails/day
- Google Workspace: Unlimited

For a small booking system, any of these is plenty.

### Q: Can I use bookings@gairalabs.com?
**A:** Yes! Two options:
1. **Google Workspace** ($6-12/month) - Professional email
2. **Email Forwarding** - Create bookings@gairalabs.com that forwards to your Gmail

### Q: Will emails go to spam?
**A:** Usually no. If they do:
- Verify your sender email matches `EMAIL_HOST_USER`
- For custom domains, set up SPF/DKIM records
- Templates are already designed to avoid spam triggers

### Q: I'm getting rate limited
**A:** You've hit daily email limit. Solutions:
- Wait until next day (limit resets at midnight UTC)
- Upgrade to Google Workspace (unlimited)
- Move to professional email service

### Q: How do I test locally?
**A:** Create `.env` file and run:
```bash
python ccweblab/manage.py shell
```

Then:
```python
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'your-email@gmail.com', ['recipient@example.com'])
```

---

## 📋 Checklist: Gmail Setup

### Before You Start
- [ ] You have a Gmail account (free or Workspace)
- [ ] You have access to Render dashboard for production

### Gmail Account Setup
- [ ] Go to https://myaccount.google.com
- [ ] Enable 2-Step Verification (Security → 2-Step Verification)
- [ ] Create App Password (https://myaccount.google.com/apppasswords)
- [ ] Copy the 16-character password safely

### Local Testing (Optional)
- [ ] Create `.env` file in project root
- [ ] Add Gmail variables (EMAIL_HOST, EMAIL_PORT, etc.)
- [ ] Test with Django shell
- [ ] Receive test email ✅

### Production (Render)
- [ ] Go to render.com dashboard
- [ ] Select your service
- [ ] Click "Environment"
- [ ] Add all 7 email variables
- [ ] Click "Save"
- [ ] Wait for auto-redeploy (~1 minute)
- [ ] Test with actual booking
- [ ] Receive confirmation email ✅

### You're Done! 🎉
- Customers receive booking confirmation emails
- Admin receives booking notifications
- Status updates are sent automatically

---

## 🔗 Useful Links

| Task | Link |
|------|------|
| Gmail App Passwords | https://myaccount.google.com/apppasswords |
| Gmail Security | https://myaccount.google.com/security |
| Gmail Account | https://mail.google.com |
| Hotmail App Passwords | https://account.microsoft.com/account/manage-my-microsoft-account |
| Google Workspace | https://workspace.google.com |
| Render Dashboard | https://dashboard.render.com |
| Django Email Docs | https://docs.djangoproject.com/en/6.0/topics/email/ |

---

## 📞 Troubleshooting

**Issue:** "SMTP authentication failed"
```
Solution: Use App Password, not regular Gmail password
Steps:
1. Verify 2-Step Verification is enabled
2. Get new App Password from myaccount.google.com/apppasswords
3. Paste exactly with spaces
```

**Issue:** "Connection refused" or "Network error"
```
Solution: Wrong port or TLS not enabled
Check:
- EMAIL_PORT=587 (not 465)
- EMAIL_USE_TLS=True
- Network allows outbound SMTP
```

**Issue:** "Emails not arriving"
```
Solution: Check spam folder or sender address
Try:
1. Send to different email address
2. Check spam/promotions folder
3. Verify DEFAULT_FROM_EMAIL matches EMAIL_HOST_USER
```

**Issue:** "Too many emails" error
```
Solution: You've hit the daily limit (500 Gmail, 1000 Hotmail)
Options:
- Use Google Workspace (unlimited)
- Wait until tomorrow (limit resets at midnight UTC)
- Batch emails over multiple days
```

---

## ✨ Pro Tips

1. **Use descriptive sender name:**
   ```
   DEFAULT_FROM_EMAIL="Gaira Labs Bookings <your-email@gmail.com>"
   ```

2. **Monitor email delivery:**
   - Gmail: Check "Sent Mail" folder
   - Render: Check deployment logs
   - Test with your own email first

3. **Keep passwords secure:**
   - Use .env files (never commit to git)
   - Use different App Passwords for different services
   - Rotate passwords monthly

4. **Professional setup:**
   - Use Google Workspace for gairalabs.com
   - Set up SPF/DKIM records
   - Use branded email templates

---

**Need more help?** See the detailed guides:
- `SETUP_EMAIL.md` - General email setup
- `SETUP_EMAIL_GMAIL.md` - Gmail-specific details
