"""
Auth domain APIs.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from api.authentication.services import (
    user_register, user_activate, user_login, 
    password_reset_request, password_reset_confirm
)
from api.authentication.selectors import user_get_login_data
from api.authentication.serializers import (
    UserRegistrationInputSerializer,
    UserActivationInputSerializer,
    UserLoginInputSerializer,
    PasswordResetRequestInputSerializer,
    PasswordResetConfirmInputSerializer,
    UserOutputSerializer,
    LoginOutputSerializer,
    ActivationOutputSerializer,
    PasswordResetOutputSerializer,
    RegistrationOutputSerializer
)


class UserRegistrationApi(APIView):
    """
    User registration endpoint
    
    Creates a new inactive user account and sends activation email.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        operation_id='auth_register',
        summary='Register a new user (inactive by default)',
        description='Creates a new inactive user account and sends activation email.',
        request=UserRegistrationInputSerializer,
        responses={
            201: RegistrationOutputSerializer,
            400: {'description': 'Validation error'}
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserRegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Filter out confirm_password before calling service
        validated_data = serializer.validated_data.copy()
        validated_data.pop('confirm_password', None)
        
        # Register user (creates inactive account)
        user = user_register(**validated_data)
        
        return Response(
            {
                'message': 'Account created successfully. Please check your email for activation link.',
                'user': UserOutputSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class UserActivationApi(APIView):
    """
    User activation endpoint
    
    Activates user account using token from email.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        operation_id='auth_activate',
        summary='Activate user account',
        description='Activates user account using token from activation email.',
        request=UserActivationInputSerializer,
        responses={
            200: ActivationOutputSerializer,
            400: {'description': 'Invalid or expired token'}
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserActivationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Activate user (service returns dict with tokens and user data)
        activation_data = user_activate(token=serializer.validated_data['token'])

        return Response(
            ActivationOutputSerializer({
                'message': 'Account activated successfully!',
                'access': activation_data['access'],
                'refresh': activation_data['refresh'],
                'user': activation_data['user']
            }).data,
            status=status.HTTP_200_OK
        )


class UserLoginApi(APIView):
    """
    User login endpoint
    
    Authenticates user and returns JWT tokens.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        operation_id='auth_login',
        summary='Login with username and password',
        description='Authenticates user and returns JWT tokens.',
        request=UserLoginInputSerializer,
        responses={
            200: LoginOutputSerializer,
            400: {'description': 'Invalid credentials or account not activated'}
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Authenticate user
        login_data = user_login(**serializer.validated_data)
        
        return Response(
            LoginOutputSerializer(login_data).data,
            status=status.HTTP_200_OK
        )


class UserMeApi(APIView):
    """
    Get current user details
    
    Returns authenticated user's profile information.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        operation_id='auth_me',
        summary='Get current authenticated user',
        description='Returns authenticated user profile information.',
        responses={
            200: UserOutputSerializer,
            401: {'description': 'Authentication required'}
        },
        tags=['Authentication']
    )
    def get(self, request):
        user_data = user_get_login_data(user=request.user)
        return Response(user_data)


class PasswordResetRequestApi(APIView):
    """
    Password reset request endpoint
    
    Sends password reset email to user.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        operation_id='auth_password_reset_request',
        summary='Request password reset',
        description='Sends password reset email to user.',
        request=PasswordResetRequestInputSerializer,
        responses={
            200: PasswordResetOutputSerializer
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = PasswordResetRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Send password reset email
        password_reset_request(email=serializer.validated_data['email'])
        
        return Response(
            PasswordResetOutputSerializer({
                'message': 'If an account with this email exists, a password reset link has been sent.'
            }).data,
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmApi(APIView):
    """
    Password reset confirmation endpoint
    
    Resets user password using token from email.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        operation_id='auth_password_reset_confirm',
        summary='Confirm password reset',
        description='Resets user password using token from email.',
        request=PasswordResetConfirmInputSerializer,
        responses={
            200: PasswordResetOutputSerializer,
            400: {'description': 'Invalid/expired token or validation error'}
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = PasswordResetConfirmInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Filter out confirm_password before calling service
        validated_data = serializer.validated_data.copy()
        validated_data.pop('confirm_password', None)
        
        try:
            # Reset password
            password_reset_confirm(**validated_data)
            
            return Response(
                PasswordResetOutputSerializer({
                    'message': 'Password reset successfully! You can now login with your new password.'
                }).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Let the custom exception handler deal with the error
            raise


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh endpoint

    Takes a refresh type JSON web token and returns an access type JSON web token if
    the refresh token is valid.
    """
    @extend_schema(
        operation_id='auth_token_refresh',
        summary='Refresh JWT access token',
        description='Takes a refresh token and returns a new access token.',
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
