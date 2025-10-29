"""
Auth domain selectors.
"""
from typing import Optional
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from api.authentication.models import CustomUser

User = get_user_model()


def user_get_by_username(*, username: str) -> CustomUser:
    """
    Get user by username.
    
    Args:
        username: Username to search for
        
    Returns:
        User instance
        
    Raises:
        CustomUser.DoesNotExist: If user not found
    """
    return CustomUser.objects.get(username=username)


def user_get_by_email(*, email: str) -> CustomUser:
    """
    Get user by email.
    
    Args:
        email: Email address to search for
        
    Returns:
        User instance
        
    Raises:
        CustomUser.DoesNotExist: If user not found
    """
    return CustomUser.objects.get(email=email)


def user_get_by_id(*, user_id: int) -> CustomUser:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        
    Returns:
        User instance
        
    Raises:
        CustomUser.DoesNotExist: If user not found
    """
    return CustomUser.objects.get(id=user_id)


def user_exists_by_username(*, username: str) -> bool:
    """
    Check if user exists by username.
    
    Args:
        username: Username to check
        
    Returns:
        True if user exists, False otherwise
    """
    return CustomUser.objects.filter(username=username).exists()


def user_exists_by_email(*, email: str) -> bool:
    """
    Check if user exists by email.
    
    Args:
        email: Email to check
        
    Returns:
        True if user exists, False otherwise
    """
    return CustomUser.objects.filter(email=email).exists()


def user_get_login_data(*, user: CustomUser) -> dict:
    """
    Get user data for login response.
    
    Args:
        user: User instance
        
    Returns:
        Dictionary with user data for login
    """
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
    }
