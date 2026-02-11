# notification_service.py
# Central place for sending notifications
# For now -> EMAIL
# Later -> Firebase / WhatsApp plug-in ready

from email_service import send_email


# ================= USER NOTIFICATION =================
def notify_user(email, subject, body):
    """
    Send notification to user.
    Currently email.
    Later we will plug Firebase here.
    """
    print("📨 Sending USER notification...")
    try:
        send_email(email, subject, body)
        print(f"✅ User notification sent to {email}")
    except Exception as e:
        print(f"❌ Failed to send user notification to {email}: {e}")
        # Don't crash the application, just log the error


# ================= DOCTOR NOTIFICATION =================
def notify_doctor(email, subject, body):
    """
    Send notification to doctor.
    Currently email.
    Later WhatsApp/Firebase ready.
    """
    print("📨 Sending DOCTOR notification...")
    try:
        send_email(email, subject, body)
        print(f"✅ Doctor notification sent to {email}")
    except Exception as e:
        print(f"❌ Failed to send doctor notification to {email}: {e}")
        # Don't crash the application, just log the error


# ================= GENERAL EMAIL FUNCTION =================
def send_email_notification(to_email, subject, body):
    """
    General email sending function with error handling
    """
    print(f"📧 Attempting to send email to {to_email}")
    try:
        send_email(to_email, subject, body)
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email sending failed to {to_email}: {e}")
        return False
