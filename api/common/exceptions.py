"""
Common exceptions for the API.
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class BusinessLogicError(APIException):
    """Base exception for business logic errors"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business logic error occurred.'
    default_code = 'business_logic_error'


class UserAlreadyExistsError(BusinessLogicError):
    """Exception raised when user already exists"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User with this username or email already exists.'
    default_code = 'user_already_exists'


class InvalidCredentialsError(BusinessLogicError):
    """Exception raised when credentials are invalid"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid credentials provided.'
    default_code = 'invalid_credentials'


class AccountNotActivatedError(BusinessLogicError):
    """Exception raised when account is not activated"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Account is not activated. Please check your email for activation link.'
    default_code = 'account_not_activated'


class InvalidTokenError(BusinessLogicError):
    """Exception raised when token is invalid"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid or malformed token.'
    default_code = 'invalid_token'


class TokenExpiredError(BusinessLogicError):
    """Exception raised when token has expired"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token has expired. Please request a new one.'
    default_code = 'token_expired'


class WeakPasswordError(BusinessLogicError):
    """Exception raised when password doesn't meet strength requirements"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Password does not meet strength requirements.'
    default_code = 'weak_password'


class UserNotFoundError(BusinessLogicError):
    """Exception raised when user is not found"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found.'
    default_code = 'user_not_found'


class EmailSendingError(BusinessLogicError):
    """Exception raised when email sending fails"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Failed to send email. Please try again later.'
    default_code = 'email_sending_error'


class NotFoundError(BusinessLogicError):
    """Exception raised when a resource is not found"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'
