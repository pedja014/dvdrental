"""
URL configuration for dvdrental_project project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="DVD Rental API",
        default_version='v1',
        description="""
        DVD Rental Management System API
        
        This API provides complete CRUD operations for managing a DVD rental business.
        
        ## Authentication
        This API uses JWT (JSON Web Token) authentication. To access protected endpoints:
        1. Register a new user at `/api/auth/register/`
        2. Login at `/api/auth/login/` to get access and refresh tokens
        3. Include the access token in the Authorization header: `Bearer <token>`
        4. Refresh expired tokens at `/api/auth/token/refresh/`
        
        ## User Roles
        - **admin**: Full access to all endpoints
        - **staff**: Can manage inventory, rentals, and view customer data
        - **customer**: Can view catalog and manage own rentals
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@dvdrental.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Swagger documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

