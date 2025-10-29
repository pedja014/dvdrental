"""
Email sending functions for auth operations (plain text only).
"""
from django.core.mail import send_mail
from django.conf import settings

from api.common.exceptions import EmailSendingError


def _get_site_name() -> str:
    return getattr(settings, 'SITE_NAME', 'DVD Rental')


def send_activation_email(user, activation_url):
    """
    Send account activation email (plain text) containing the activation link.
    """
    subject = f"Activate your {_get_site_name()} account"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        f"Thanks for registering at {_get_site_name()}.\n"
        f"Please activate your account by opening this link:\n{activation_url}\n\n"
        f"If you did not request this, you can ignore this email."
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise EmailSendingError(f"Failed to send activation email: {str(e)}")


def send_password_reset_email(user, reset_url):
    """
    Send password reset email (plain text) containing the reset link.
    """
    subject = f"Reset your {_get_site_name()} password"
    message = (
        f"Hello {user.first_name or user.username},\n\n"
        f"We received a request to reset your password.\n"
        f"You can set a new password by opening this link:\n{reset_url}\n\n"
        f"If you did not request a password reset, you can ignore this email."
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise EmailSendingError(f"Failed to send password reset email: {str(e)}")
