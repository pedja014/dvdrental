"""
Custom exception handler for the API.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    
    Args:
        exc: The exception that was raised
        context: The context in which the exception was raised
        
    Returns:
        Response: Formatted error response
    """
    # Handle Django ValidationError specifically
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                'error': {
                    'type': 'ValidationError',
                    'message': 'Validation failed',
                    'code': 'validation_error',
                    'status_code': 400,
                    'fields': exc.message_dict if hasattr(exc, 'message_dict') else {'non_field_errors': [str(exc)]}
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get the standard error response
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the error response format
        custom_response_data = {
            'error': {
                'type': exc.__class__.__name__,
                'message': response.data.get('detail', str(exc)),
                'code': getattr(exc, 'default_code', 'unknown_error'),
                'status_code': response.status_code
            }
        }
        
        # Add field-specific errors if they exist
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['error']['fields'] = response.data
        
        # Log the error for debugging
        logger.error(f"API Error: {exc.__class__.__name__} - {str(exc)}", exc_info=True)
        
        response.data = custom_response_data
    
    return response
