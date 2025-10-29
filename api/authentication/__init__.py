"""
Authentication domain.
"""
# Note: All services, selectors, and models are available via direct import
# when needed, but not imported here to avoid circular import issues during app loading
# 
# Usage:
# from api.authentication.services import user_register
# from api.authentication.selectors import user_exists_by_username
# from api.authentication.models import CustomUser
# or
# from django.contrib.auth import get_user_model
# User = get_user_model()  # This will be CustomUser
