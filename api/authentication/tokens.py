"""
Token generation and validation for auth operations.
"""
import time
from django.core import signing
from django.conf import settings
from django.contrib.auth import get_user_model

from api.common.exceptions import InvalidTokenError, TokenExpiredError, UserNotFoundError

User = get_user_model()

# Token expiration times (in seconds)
ACTIVATION_TOKEN_EXPIRY = 7 * 24 * 60 * 60  # 7 days
PASSWORD_RESET_TOKEN_EXPIRY = 24 * 60 * 60  # 24 hours


def generate_activation_token(user):
    """
    Generate activation token for user account.
    
    Args:
        user: User instance
        
    Returns:
        str: Signed activation token
    """
    data = {
        'user_id': user.id,
        'username': user.username,
        'timestamp': int(time.time()),
        'type': 'activation'
    }
    
    return signing.dumps(data, salt='activation-token', compress=True)


def validate_activation_token(token):
    """
    Validate activation token and return user.
    
    Args:
        token: Activation token string
        
    Returns:
        User: User instance
        
    Raises:
        InvalidTokenError: If token is invalid
        TokenExpiredError: If token has expired
        UserNotFoundError: If user doesn't exist
    """
    try:
        data = signing.loads(token, salt='activation-token', max_age=ACTIVATION_TOKEN_EXPIRY)
    except signing.BadSignature:
        raise InvalidTokenError("Invalid activation token.")
    except signing.SignatureExpired:
        raise TokenExpiredError("Activation token has expired.")
    
    if data.get('type') != 'activation':
        raise InvalidTokenError("Invalid token type.")
    
    try:
        user = User.objects.get(id=data['user_id'], username=data['username'])
    except User.DoesNotExist:
        raise UserNotFoundError("User not found.")
    
    return user


def generate_password_reset_token(user):
    """
    Generate password reset token for user.
    
    Args:
        user: User instance
        
    Returns:
        str: Signed password reset token
    """
    data = {
        'user_id': user.id,
        'username': user.username,
        'timestamp': int(time.time()),
        'type': 'password_reset'
    }
    
    return signing.dumps(data, salt='password-reset-token', compress=True)


def validate_password_reset_token(token):
    """
    Validate password reset token and return user.
    
    Args:
        token: Password reset token string
        
    Returns:
        User: User instance
        
    Raises:
        InvalidTokenError: If token is invalid
        TokenExpiredError: If token has expired
        UserNotFoundError: If user doesn't exist
    """
    try:
        data = signing.loads(token, salt='password-reset-token', max_age=PASSWORD_RESET_TOKEN_EXPIRY)
    except signing.BadSignature:
        raise InvalidTokenError("Invalid password reset token.")
    except signing.SignatureExpired:
        raise TokenExpiredError("Password reset token has expired.")
    
    if data.get('type') != 'password_reset':
        raise InvalidTokenError("Invalid token type.")
    
    try:
        user = User.objects.get(id=data['user_id'], username=data['username'])
    except User.DoesNotExist:
        raise UserNotFoundError("User not found.")
    
    return user
