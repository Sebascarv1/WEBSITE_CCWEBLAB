# Gmail App Passwords Not Available - Troubleshooting

## "The setting that you are looking for is not available for your account"

This error occurs when trying to access App Passwords. Here's how to fix it:

---

## ✅ Common Causes & Solutions

### 1. You Don't Have 2-Step Verification Enabled

**This is the #1 reason this error occurs.**

**Fix:**
1. Go to https://myaccount.google.com/security
2. Scroll down to "How you sign in to Google"
3. Click **2-Step Verification**
4. Follow all the prompts (phone verification, etc.)
5. Once complete, go back to https://myaccount.google.com/apppasswords
6. Now it should work! ✅

---

### 2. You're Using a Work/Business Google Account

**Google Workspace (work accounts) handles App Passwords differently.**

If you see your email as:
- `name@company.com` 
- `name@yourcompany.co.uk`
- Any non-Gmail domain

**Fix:**
Your admin must enable "Allow less secure app access" or you need a regular `@gmail.com` account for this.

**Better Option:** Use a personal Gmail account instead.

---

### 3. You're On a Family Link Account

**Google Family Link doesn't support App Passwords.**

**Fix:**
- Ask the family admin to enable it
- Or use a different personal Gmail account

---

### 4. You're Using the Wrong Google Account

**Make sure you're logged into the correct account.**

**Check:**
1. Look at the top-right corner of https://myaccount.google.com
2. Click your profile picture
3. Make sure it's the email you want to use for bookings

**If wrong account:**
1. Click **Sign out**
2. Click **Sign in as a different account**
3. Log in with your personal `@gmail.com` account
4. Try App Passwords again

---

## 🔄 Alternative: Use an App-Specific Password (Older Method)

If App Passwords isn't available, try this older approach:

### Step 1: Enable "Less Secure Apps"

⚠️ **Note:** This method is being deprecated by Google

1. Go to https://myaccount.google.com/lesssecureapps
2. Toggle **ON** "Allow less secure app access"
3. Use your regular Gmail password in the `.env` file

### Settings:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-actual-gmail-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**⚠️ Warning:** This is less secure and Google may disable it soon.

---

## 💡 Recommended Solution

### Create a Fresh Personal Gmail Account

This is the easiest and most secure approach:

1. Go to https://accounts.google.com/signup
2. Create a new personal Gmail account
   - Example: `bookings@gmail.com`
   - Or: `yourname.bookings@gmail.com`
3. Enable 2-Step Verification on this new account
4. Create App Password on this new account
5. Use this email in your `.env` file

**Advantages:**
- ✅ Works immediately
- ✅ Secure (uses App Passwords)
- ✅ Dedicated to your booking system
- ✅ Easy to manage separately

---

## 🚀 Step-by-Step: New Gmail Account + App Passwords

### 1. Create New Gmail Account (5 minutes)

```
1. Go to https://accounts.google.com/signup
2. Fill in:
   - First name: Gaira
   - Last name: Labs (or your name)
   - Email: bookings@gmail.com (or yourname.bookings@gmail.com)
   - Password: Strong password (save it!)
3. Add recovery email and phone
4. Complete verification
5. Click "Agree and create account"
```

### 2. Enable 2-Step Verification (2 minutes)

```
1. Go to https://myaccount.google.com/security
2. Find "How you sign in to Google"
3. Click "2-Step Verification"
4. Select phone verification method
5. Complete all prompts
6. Done! ✅
```

### 3. Create App Password (1 minute)

```
1. Go to https://myaccount.google.com/apppasswords
2. Select:
   - App: Mail
   - Device: Windows Computer (or your OS)
3. Click "Generate"
4. Copy the 16-character password
```

### 4. Update Your `.env` File

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=bookings@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=bookings@gmail.com
CONTACT_TO_EMAIL=admin@gairalabs.com
```

### 5. Deploy to Render

```
1. Go to https://dashboard.render.com
2. Select your service
3. Click "Environment"
4. Add all 7 email variables above
5. Click "Save"
6. Wait for auto-redeploy (~1 minute)
7. Test with a booking!
```

---

## ❓ FAQ

### Q: Do I need a separate Gmail account?
**A:** No, but it's recommended for security. You can use your personal Gmail if it meets the requirements (2-Step Verification enabled).

### Q: Will my old Gmail account work now?
**A:** Only if you enable 2-Step Verification first. Then App Passwords becomes available.

### Q: How do I enable 2-Step Verification on my existing account?

1. Go to https://myaccount.google.com/security
2. Scroll to "How you sign in to Google"
3. Click "2-Step Verification"
4. Select verification method (phone, security key, etc.)
5. Complete the process
6. Try App Passwords again

### Q: Why is this security feature even required?
**A:** App Passwords are more secure than giving your real password to apps. They can be revoked independently and only work for the specified app/device.

### Q: Can I use Hotmail/Outlook instead?
**A:** Yes! Same setup, different server:
```
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_HOST_USER=your-email@hotmail.com
```
Same 2-Step Verification → App Password process.

### Q: What if I'm still getting the error?
**Try this order:**
1. [ ] Log out completely (close all tabs)
2. [ ] Log back in with correct email
3. [ ] Go to https://myaccount.google.com (confirm you're signed in)
4. [ ] Go to Security → 2-Step Verification (enable if not done)
5. [ ] Go to https://myaccount.google.com/apppasswords
6. [ ] If still error → Create a new Gmail account and try again

---

## 🆘 Still Not Working?

If you've tried everything above and still getting errors:

### Option A: Contact Google Support
- Go to https://support.google.com/accounts
- Search "App passwords"
- Click "Get help from the community"

### Option B: Use a Simpler Email Service
- **Brevo (formerly Sendinblue):** Free tier with good SMTP support
- **Mailgun:** Free tier for testing
- **SendGrid:** Free tier available

These services are specifically designed for transactional emails like booking confirmations.

---

## ✅ Checklist Before Trying App Passwords

- [ ] You're using a personal `@gmail.com` account (not work/school)
- [ ] 2-Step Verification is ENABLED on that account
- [ ] You're logged into the correct Gmail account
- [ ] You're accessing https://myaccount.google.com/apppasswords (exact URL)
- [ ] The page shows the "App" and "Device" dropdown menus

If all checkboxes pass, App Passwords should be available!

---

## Summary

| Issue | Solution | Time |
|-------|----------|------|
| "Setting not available" error | Enable 2-Step Verification first | 5 min |
| Work/Business account | Create personal Gmail account | 10 min |
| Still not working | Create new dedicated Gmail | 15 min |

**Easiest path:** Create a new personal Gmail account, enable 2-Step Verification, then create App Password. Takes ~15 minutes total.

---

## Next Steps

1. **Create new Gmail** (or verify 2-Step on existing)
2. **Enable 2-Step Verification**
3. **Create App Password**
4. **Update .env file**
5. **Deploy to Render**
6. **Test with a booking!** ✅

---

**Still confused?** The quick reference has step-by-step images and links:
👉 See `EMAIL_SETUP_QUICK_REFERENCE.md`
