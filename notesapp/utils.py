# notesapp/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, code):
    """
    Sends an email with the verification code to the user.
    """
    subject = 'Verify Your Email Address'

    # This is the email message body. We use an f-string to include the code.
    message = f"""
    Hello,

    Thank you for registering. Please use the following 6-digit code to verify your email address:

    {code}

    This code will expire in 15 minutes.

    If you did not request this, please ignore this email.
    """

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print(f"Verification email sent to {email}") # For debugging
    except Exception as e:
        print(f"Error sending email: {e}") # For debugging