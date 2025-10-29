"""
Auth domain URLs.
"""
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from api.authentication.apis import (
    UserRegistrationApi,
    UserActivationApi,
    UserLoginApi,
    UserMeApi,
    PasswordResetRequestApi,
    PasswordResetConfirmApi,
    CustomTokenRefreshView
)

@api_view(['GET'])
@extend_schema(
    operation_id='auth_root',
    summary='Authentication endpoints overview',
    description='Shows all available authentication endpoints.',
    tags=['Authentication']
)
def auth_root(request):
    """Authentication endpoints overview"""
    return Response({
        'message': 'Authentication endpoints',
        'endpoints': {
            'register': '/api/auth/register/',
            'activate': '/api/auth/activate/',
            'login': '/api/auth/login/',
            'me': '/api/auth/me/',
            'password_reset': '/api/auth/password-reset/',
            'password_reset_confirm': '/api/auth/password-reset/confirm/',
            'token_refresh': '/api/auth/token/refresh/'
        }
    })

urlpatterns = [
    # Auth root
    path('', auth_root, name='auth-root'),
    
    # Authentication endpoints
    path('register/', UserRegistrationApi.as_view(), name='auth-register'),
    path('activate/', UserActivationApi.as_view(), name='auth-activate'),
    path('login/', UserLoginApi.as_view(), name='auth-login'),
    path('me/', UserMeApi.as_view(), name='auth-me'),
    
    # Password reset endpoints
    path('password-reset/', PasswordResetRequestApi.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmApi.as_view(), name='password-reset-confirm'),
    
    # Token refresh
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
]
