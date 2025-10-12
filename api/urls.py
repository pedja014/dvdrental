from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView, UserRegistrationView, UserViewSet,
    ActorViewSet, CategoryViewSet, CountryViewSet, CityViewSet,
    AddressViewSet, LanguageViewSet, FilmViewSet, FilmActorViewSet,
    FilmCategoryViewSet, StoreViewSet, StaffViewSet, CustomerViewSet,
    InventoryViewSet, RentalViewSet, PaymentViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'cities', CityViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'languages', LanguageViewSet)
router.register(r'films', FilmViewSet)
router.register(r'film-actors', FilmActorViewSet)
router.register(r'film-categories', FilmCategoryViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'rentals', RentalViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('', include(router.urls)),
]

