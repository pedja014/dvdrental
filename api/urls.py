from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """API root endpoint with available endpoints"""
    return Response({
        'message': 'DVD Rental API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'authentication': '/api/auth/',
            'films': '/api/films/',
            'categories': '/api/categories/',
            'payments': '/api/payments/',
            'rentals': '/api/rentals/',
            'analytics': '/api/analytics/',
            'documentation': {
                'swagger': '/api/docs/',
                'redoc': '/api/redoc/',
                'schema': '/api/schema/'
            }
        },
        'note': 'This is a public endpoint. Authentication is required for protected endpoints.'
    })

urlpatterns = [
    # API root
    path('', api_root, name='api-root'),
    
    # Authentication domain
    path('auth/', include('api.authentication.urls')),
    
    # Business domains
    path('films/', include('api.films.urls')),
    path('categories/', include('api.categories.urls')),
    path('payments/', include('api.payments.urls')),
    path('rentals/', include('api.rentals.urls')),
    
    # Analytics domain
    path('analytics/', include('api.analytics.urls')),
]

