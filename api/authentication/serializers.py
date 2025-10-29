"""
Auth domain serializers.
"""
import re
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.authentication.models import CustomUser
from api.authentication.selectors import user_exists_by_username, user_exists_by_email


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user role in token"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['role'] = user.role
        token['username'] = user.username
        token['email'] = user.email
        return token


class UserRegistrationInputSerializer(serializers.Serializer):
    """
    Input serializer for user registration
    
    Required fields: username, email, password, confirm_password
    Optional fields: first_name, last_name
    """
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        help_text="Username for the user account (3-150 characters, alphanumeric and underscore only)"
    )
    email = serializers.EmailField(
        help_text="Email address for the user account"
    )
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Password for the user account (minimum 8 characters)"
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text="Confirm password (must match password)"
    )
    first_name = serializers.CharField(
        max_length=30, 
        required=False, 
        allow_blank=True,
        help_text="User's first name (optional)"
    )
    last_name = serializers.CharField(
        max_length=30, 
        required=False, 
        allow_blank=True,
        help_text="User's last name (optional)"
    )
    

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class UserActivationInputSerializer(serializers.Serializer):
    """Input serializer for user activation"""
    token = serializers.CharField(
        help_text="Activation token received via email"
    )


class UserLoginInputSerializer(serializers.Serializer):
    """Input serializer for user login"""
    username = serializers.CharField(
        help_text="Username or email address"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Password"
    )


class PasswordResetRequestInputSerializer(serializers.Serializer):
    """Input serializer for password reset request"""
    email = serializers.EmailField(
        help_text="Email address to send reset link to"
    )


class PasswordResetConfirmInputSerializer(serializers.Serializer):
    """Input serializer for password reset confirmation"""
    token = serializers.CharField(
        help_text="Password reset token received via email"
    )
    new_password = serializers.CharField(
        min_length=8,
        help_text="New password (minimum 8 characters)"
    )
    confirm_password = serializers.CharField(
        help_text="Confirm new password"
    )
    
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class UserOutputSerializer(serializers.ModelSerializer):
    """Output serializer for user data"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class LoginOutputSerializer(serializers.Serializer):
    """Output serializer for login response"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserOutputSerializer()


class ActivationOutputSerializer(serializers.Serializer):
    """Output serializer for activation response"""
    message = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserOutputSerializer()


class PasswordResetOutputSerializer(serializers.Serializer):
    """Output serializer for password reset response"""
    message = serializers.CharField()


class RegistrationOutputSerializer(serializers.Serializer):
    """Output serializer for registration response"""
    message = serializers.CharField()
    user = UserOutputSerializer()
