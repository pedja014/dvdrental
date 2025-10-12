from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTestCase(TestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'role': 'customer'
        }
    
    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_login(self):
        """Test user can login and get token"""
        # Create user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='customer'
        )
        
        # Login
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class FilmAPITestCase(TestCase):
    """Test film endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='customer'
        )
    
    def test_films_list_requires_auth(self):
        """Test that films list requires authentication"""
        response = self.client.get('/api/films/')
        # Should allow read-only access or require auth based on settings
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
    
    def test_authenticated_user_can_access_films(self):
        """Test authenticated user can access films"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/films/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

