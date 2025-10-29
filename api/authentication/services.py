"""
Auth domain services.
"""
from typing import Dict, Any
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.authentication.models import CustomUser
from api.authentication.validators import validate_password_strength
from api.common.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, AccountNotActivatedError,
    UserNotFoundError, EmailSendingError, WeakPasswordError
)
from api.authentication.tokens import generate_activation_token, validate_activation_token, generate_password_reset_token, validate_password_reset_token
from api.authentication.emails import send_activation_email, send_password_reset_email
from api.authentication.selectors import user_exists_by_username, user_exists_by_email, user_get_by_email

User = get_user_model()


@transaction.atomic
def user_register(
    *,
    username: str,
    email: str,
    password: str,
    first_name: str = '',
    last_name: str = ''
) -> CustomUser:
    """
    Register new inactive user and send activation email.
    
    Args:
        username: Username for the user
        email: Email address
        password: Password (will be hashed)
        first_name: First name
        last_name: Last name
        
    Returns:
        Created user instance
        
    Raises:
        UserAlreadyExistsError: If username/email already exists
        EmailSendingError: If activation email fails to send
        WeakPasswordError: If password doesn't meet strength requirements
    """
    
    # Check for existing username/email first (before creating object)
    if user_exists_by_username(username=username):
        raise UserAlreadyExistsError("A user with this username already exists.")
    
    if user_exists_by_email(email=email):
        raise UserAlreadyExistsError("A user with this email already exists.")
    
    # Validate password strength before hashing
    try:
        validate_password_strength(password)
    except DjangoValidationError as e:
        raise WeakPasswordError(str(e.message_dict.get('password', ['Weak password'])[0]))
    
    # Create user instance
    user = CustomUser(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        is_active=False,
        role='customer'
    )
    
    # Set password (hashes it)
    user.set_password(password)
    
    # Validate all business rules
    try:
        user.full_clean()
    except DjangoValidationError as e:
        # Convert Django ValidationError to our custom exception
        raise UserAlreadyExistsError(str(e))
    
    # Save user
    user.save()
    
    # Generate and send activation email
    activation_token = generate_activation_token(user)
    try:
        activation_url = f"{settings.FRONTEND_URL}/activate?token={activation_token}"
        send_activation_email(user, activation_url)
    except EmailSendingError:
        raise EmailSendingError("Failed to send activation email. Please try again later.")
    
    return user


@transaction.atomic
def user_activate(*, token: str) -> Dict[str, Any]:
    """
    Activate user account using token.
    
    Args:
        token: Activation token
        
    Returns:
        Dictionary containing user data and JWT tokens
        
    Raises:
        InvalidTokenError: If token is invalid
        TokenExpiredError: If token has expired
        UserNotFoundError: If user doesn't exist
        AccountNotActivatedError: If account is already active
    """
    user = validate_activation_token(token)
    
    if user.is_active:
        raise AccountNotActivatedError("Account is already activated.")
    
    user.is_active = True
    user.save()
    
    refresh = RefreshToken.for_user(user)
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
        },
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def user_login(*, username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate user and return JWT tokens.
    
    Args:
        username: Username or email
        password: Password
        
    Returns:
        Dictionary with tokens and user data
        
    Raises:
        InvalidCredentialsError: If credentials are invalid
        AccountNotActivatedError: If account is not activated
    """
    # If an account exists but is not activated, inform explicitly
    candidate_user: CustomUser | None = None
    try:
        candidate_user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        try:
            candidate_user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            candidate_user = None

    if candidate_user and not candidate_user.is_active:
        raise AccountNotActivatedError("Account is not activated. Please check your email for activation link.")

    # Authenticate with provided credentials
    user = authenticate(username=username, password=password)

    if not user:
        raise InvalidCredentialsError("Invalid username or password.")
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    # Get user data
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
    }
    
    return {
        'access': str(access),
        'refresh': str(refresh),
        'user': user_data
    }


def password_reset_request(*, email: str) -> None:
    """
    Send password reset email.
    
    Args:
        email: Email address
        
    Raises:
        UserNotFoundError: If user doesn't exist
        EmailSendingError: If email sending fails
    """
    try:
        user = user_get_by_email(email=email)
    except CustomUser.DoesNotExist:
        # Don't reveal if email exists or not for security
        return
    
    # Generate password reset token
    reset_token = generate_password_reset_token(user)
    
    # Send password reset email
    try:
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        send_password_reset_email(user, reset_url)
    except EmailSendingError as e:
        raise EmailSendingError(f"Failed to send password reset email: {str(e)}")


@transaction.atomic
def password_reset_confirm(*, token: str, new_password: str) -> None:
    """
    Reset password using token.
    
    Args:
        token: Password reset token
        new_password: New password
        
    Raises:
        InvalidTokenError: If token is invalid
        TokenExpiredError: If token has expired
        UserNotFoundError: If user doesn't exist
        WeakPasswordError: If password doesn't meet strength requirements
        ValidationError: If new password matches current password
    """
    user = validate_password_reset_token(token)
    
    # Check if new password is different from current password
    if user.check_password(new_password):
        raise DjangoValidationError({'new_password': 'New password must be different from your current password.'})
    
    # Validate password strength
    try:
        validate_password_strength(new_password)
    except DjangoValidationError as e:
        raise WeakPasswordError(str(e.message_dict.get('password', ['Weak password'])[0]))
    
    user.set_password(new_password)
    user.save()
