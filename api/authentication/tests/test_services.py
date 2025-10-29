"""
Auth domain service tests.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

from api.authentication.services import (
    user_register, user_activate, user_login,
    password_reset_request, password_reset_confirm
)
from api.authentication.tests.factories import UserFactory, InactiveUserFactory
from api.common.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, AccountNotActivatedError,
    InvalidTokenError, TokenExpiredError, UserNotFoundError
)

User = get_user_model()


class UserRegisterTestCase(TestCase):
    """Test user registration service"""
    
    def test_user_register_creates_inactive_user(self):
        """Test creating inactive user with valid data"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        with patch('api.auth.services.send_activation_email') as mock_email:
            user = user_register(**user_data)
            
            self.assertIsInstance(user, CustomUser)
            self.assertEqual(user.username, 'testuser')
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.first_name, 'Test')
            self.assertEqual(user.last_name, 'User')
            self.assertFalse(user.is_active)  # Should be inactive
            self.assertEqual(user.role, 'customer')  # Default role
            self.assertTrue(user.check_password('TestPass123!'))
            
            # Check that activation email was sent
            mock_email.assert_called_once()
    
    def test_user_register_with_duplicate_username_raises_error(self):
        """Test creating user with duplicate username"""
        UserFactory(username='existinguser')
        
        user_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'TestPass123!'
        }
        
        with self.assertRaises(UserAlreadyExistsError):
            user_register(**user_data)
    
    def test_user_register_with_duplicate_email_raises_error(self):
        """Test creating user with duplicate email"""
        UserFactory(email='existing@example.com')
        
        user_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'TestPass123!'
        }
        
        with self.assertRaises(UserAlreadyExistsError):
            user_register(**user_data)


class UserActivateTestCase(TestCase):
    """Test user activation service"""
    
    def test_user_activate_with_valid_token_activates_user(self):
        """Test activating user with valid token"""
        user = InactiveUserFactory()
        
        with patch('api.auth.tokens.validate_activation_token', return_value=user):
            activated_user = user_activate(token='valid_token')
            
            self.assertEqual(activated_user, user)
            self.assertTrue(activated_user.is_active)
    
    def test_user_activate_with_invalid_token_raises_error(self):
        """Test activating user with invalid token"""
        with patch('api.auth.tokens.validate_activation_token', side_effect=InvalidTokenError):
            with self.assertRaises(InvalidTokenError):
                user_activate(token='invalid_token')


class UserLoginTestCase(TestCase):
    """Test user login service"""
    
    def test_user_login_with_valid_credentials_returns_tokens(self):
        """Test login with valid credentials"""
        user = UserFactory(password='testpass123')
        user.set_password('testpass123')
        user.save()
        
        with patch('api.auth.services.authenticate', return_value=user):
            result = user_login(username='testuser', password='testpass123')
            
            self.assertIn('access', result)
            self.assertIn('refresh', result)
            self.assertIn('user', result)
            self.assertEqual(result['user']['username'], user.username)
    
    def test_user_login_with_invalid_credentials_raises_error(self):
        """Test login with invalid credentials"""
        with patch('api.auth.services.authenticate', return_value=None):
            with self.assertRaises(InvalidCredentialsError):
                user_login(username='testuser', password='wrongpass')
    
    def test_user_login_with_inactive_account_raises_error(self):
        """Test login with inactive account"""
        user = InactiveUserFactory()
        
        with patch('api.auth.services.authenticate', return_value=user):
            with self.assertRaises(AccountNotActivatedError):
                user_login(username='testuser', password='testpass123')


class PasswordResetTestCase(TestCase):
    """Test password reset services"""
    
    def test_password_reset_request_with_existing_email_sends_email(self):
        """Test password reset request with existing email"""
        user = UserFactory(email='test@example.com')
        
        with patch('api.auth.services.send_password_reset_email') as mock_email:
            password_reset_request(email='test@example.com')
            mock_email.assert_called_once()
    
    def test_password_reset_request_with_nonexistent_email_does_nothing(self):
        """Test password reset request with non-existent email"""
        with patch('api.auth.services.send_password_reset_email') as mock_email:
            password_reset_request(email='nonexistent@example.com')
            mock_email.assert_not_called()
    
    def test_password_reset_confirm_with_valid_token_resets_password(self):
        """Test password reset confirmation with valid token"""
        user = UserFactory()
        old_password_hash = user.password
        
        with patch('api.auth.tokens.validate_activation_token', return_value=user):
            password_reset_confirm(token='valid_token', new_password='NewPass123!')
            
            user.refresh_from_db()
            self.assertNotEqual(user.password, old_password_hash)
            self.assertTrue(user.check_password('NewPass123!'))
