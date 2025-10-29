"""
Auth domain API tests.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock

from api.authentication.tests.factories import UserFactory, InactiveUserFactory


class UserRegistrationApiTestCase(APITestCase):
    """Test user registration API"""
    
    def test_user_registration_with_valid_data_creates_user(self):
        """Test user registration with valid data"""
        url = reverse('auth-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'TestPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        with patch('api.auth.services.user_register') as mock_register:
            mock_user = UserFactory()
            mock_register.return_value = mock_user
            
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('message', response.data)
            self.assertIn('user', response.data)
            mock_register.assert_called_once()
    
    def test_user_registration_with_weak_password_returns_error(self):
        """Test user registration with weak password"""
        url = reverse('auth-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',
            'confirm_password': 'weak'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_user_registration_with_mismatched_passwords_returns_error(self):
        """Test user registration with mismatched passwords"""
        url = reverse('auth-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPass123!',
            'confirm_password': 'DifferentPass123!'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class UserActivationApiTestCase(APITestCase):
    """Test user activation API"""
    
    def test_user_activation_with_valid_token_activates_user(self):
        """Test user activation with valid token"""
        url = reverse('auth-activate')
        data = {'token': 'valid_token'}
        
        with patch('api.auth.services.user_activate') as mock_activate:
            mock_user = UserFactory()
            mock_activate.return_value = mock_user
            
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.data)
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
            self.assertIn('user', response.data)
    
    def test_user_activation_with_invalid_token_returns_error(self):
        """Test user activation with invalid token"""
        url = reverse('auth-activate')
        data = {'token': 'invalid_token'}
        
        with patch('api.auth.services.user_activate', side_effect=Exception('Invalid token')):
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginApiTestCase(APITestCase):
    """Test user login API"""
    
    def test_user_login_with_valid_credentials_returns_tokens(self):
        """Test user login with valid credentials"""
        url = reverse('auth-login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        with patch('api.auth.services.user_login') as mock_login:
            mock_login.return_value = {
                'access': 'mock_access_token',
                'refresh': 'mock_refresh_token',
                'user': {'id': 1, 'username': 'testuser'}
            }
            
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
            self.assertIn('user', response.data)
    
    def test_user_login_with_invalid_credentials_returns_error(self):
        """Test user login with invalid credentials"""
        url = reverse('auth-login')
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        
        with patch('api.auth.services.user_login', side_effect=Exception('Invalid credentials')):
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserMeApiTestCase(APITestCase):
    """Test user me API"""
    
    def test_user_me_with_authenticated_user_returns_user_data(self):
        """Test getting current user data"""
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = reverse('auth-me')
        
        with patch('api.auth.selectors.user_get_login_data') as mock_get_data:
            mock_get_data.return_value = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            
            response = self.client.get(url)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['id'], user.id)
            self.assertEqual(response.data['username'], user.username)
    
    def test_user_me_with_unauthenticated_user_returns_error(self):
        """Test getting current user data without authentication"""
        url = reverse('auth-me')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetApiTestCase(APITestCase):
    """Test password reset APIs"""
    
    def test_password_reset_request_with_valid_email_returns_success(self):
        """Test password reset request with valid email"""
        url = reverse('password-reset')
        data = {'email': 'test@example.com'}
        
        with patch('api.auth.services.password_reset_request') as mock_reset:
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.data)
            mock_reset.assert_called_once_with(email='test@example.com')
    
    def test_password_reset_confirm_with_valid_data_returns_success(self):
        """Test password reset confirmation with valid data"""
        url = reverse('password-reset-confirm')
        data = {
            'token': 'valid_token',
            'new_password': 'NewPass123!',
            'confirm_password': 'NewPass123!'
        }
        
        with patch('api.auth.services.password_reset_confirm') as mock_confirm:
            response = self.client.post(url, data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('message', response.data)
            mock_confirm.assert_called_once_with(
                token='valid_token',
                new_password='NewPass123!'
            )
