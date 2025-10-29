from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    """Custom user model with role-based access control"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    
    class Meta:
        db_table = 'api_customuser'
    
    def clean(self):
        """Validate user data according to business rules"""
        super().clean()
        
        # Validate username format
        if self.username and not re.match(r'^[a-zA-Z0-9_]+$', self.username):
            raise ValidationError({
                'username': 'Username can only contain letters, numbers, and underscores.'
            })
        
        # Validate email domain (no disposable emails)
        if self.email:
            disposable_domains = [
                '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
                'mailinator.com', 'throwaway.email', 'temp-mail.org'
            ]
            domain = self.email.split('@')[1].lower() if '@' in self.email else ''
            if domain in disposable_domains:
                raise ValidationError({
                    'email': 'Please use a valid email address (disposable domains not allowed).'
                })
    
    def __str__(self):
        return f"{self.username} ({self.role})"
