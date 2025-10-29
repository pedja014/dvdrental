"""
Auth domain test factories.
"""
import factory
from django.contrib.auth import get_user_model

from api.models import CustomUser

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating test users"""
    
    class Meta:
        model = CustomUser
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'customer'
    is_active = True


class InactiveUserFactory(factory.django.DjangoModelFactory):
    """Factory for creating inactive test users"""
    
    class Meta:
        model = CustomUser
    
    username = factory.Sequence(lambda n: f"inactive_user{n}")
    email = factory.Sequence(lambda n: f"inactive_user{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'customer'
    is_active = False


class AdminUserFactory(factory.django.DjangoModelFactory):
    """Factory for creating admin test users"""
    
    class Meta:
        model = CustomUser
    
    username = factory.Sequence(lambda n: f"admin{n}")
    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = 'admin'
    is_active = True
    is_staff = True
    is_superuser = True
