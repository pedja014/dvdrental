from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q

from .models import (
    CustomUser, Actor, Category, Country, City, Address, Language,
    Film, FilmActor, FilmCategory, Store, Staff, Customer,
    Inventory, Rental, Payment
)
from .serializers import (
    CustomTokenObtainPairSerializer, UserRegistrationSerializer, UserSerializer,
    ActorSerializer, CategorySerializer, CountrySerializer, CitySerializer,
    AddressSerializer, LanguageSerializer, FilmSerializer, FilmDetailSerializer,
    FilmActorSerializer, FilmCategorySerializer, StoreSerializer, StaffSerializer,
    CustomerSerializer, InventorySerializer, RentalSerializer, PaymentSerializer
)
from .permissions import IsAdmin, IsStaffOrAdmin, ReadOnly


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view with role information"""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users (admin only)"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user details"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ActorViewSet(viewsets.ModelViewSet):
    """ViewSet for Actor model"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    
    @action(detail=True, methods=['get'])
    def films(self, request, pk=None):
        """Get all films for a specific actor"""
        actor = self.get_object()
        film_actors = FilmActor.objects.filter(actor=actor).select_related('film')
        films = [fa.film for fa in film_actors]
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ReadOnly]
    
    @action(detail=True, methods=['get'])
    def films(self, request, pk=None):
        """Get all films in a specific category"""
        category = self.get_object()
        film_categories = FilmCategory.objects.filter(category=category).select_related('film')
        films = [fc.film for fc in film_categories]
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)


class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for Country model"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated | ReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City model"""
    queryset = City.objects.all().select_related('country')
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated | ReadOnly]


class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet for Address model"""
    queryset = Address.objects.all().select_related('city', 'city__country')
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated | ReadOnly]


class LanguageViewSet(viewsets.ModelViewSet):
    """ViewSet for Language model"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated | ReadOnly]


class FilmViewSet(viewsets.ModelViewSet):
    """ViewSet for Film model with search functionality"""
    queryset = Film.objects.all().select_related('language')
    permission_classes = [IsAuthenticated | ReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FilmDetailSerializer
        return FilmSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search films by title or description"""
        query = request.query_params.get('q', '')
        if query:
            films = self.queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            films = self.queryset
        
        page = self.paginate_queryset(films)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(films, many=True)
        return Response(serializer.data)


class FilmActorViewSet(viewsets.ModelViewSet):
    """ViewSet for FilmActor model"""
    queryset = FilmActor.objects.all().select_related('actor', 'film')
    serializer_class = FilmActorSerializer
    permission_classes = [IsStaffOrAdmin]


class FilmCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for FilmCategory model"""
    queryset = FilmCategory.objects.all().select_related('film', 'category')
    serializer_class = FilmCategorySerializer
    permission_classes = [IsStaffOrAdmin]


class StoreViewSet(viewsets.ModelViewSet):
    """ViewSet for Store model"""
    queryset = Store.objects.all().select_related('address')
    serializer_class = StoreSerializer
    permission_classes = [IsStaffOrAdmin]


class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet for Staff model"""
    queryset = Staff.objects.all().select_related('address', 'store')
    serializer_class = StaffSerializer
    permission_classes = [IsStaffOrAdmin]


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer model"""
    queryset = Customer.objects.all().select_related('address', 'store')
    serializer_class = CustomerSerializer
    permission_classes = [IsStaffOrAdmin]
    
    @action(detail=True, methods=['get'])
    def rentals(self, request, pk=None):
        """Get all rentals for a specific customer"""
        customer = self.get_object()
        rentals = Rental.objects.filter(customer=customer).select_related(
            'inventory__film', 'staff'
        )
        serializer = RentalSerializer(rentals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a specific customer"""
        customer = self.get_object()
        payments = Payment.objects.filter(customer=customer).select_related('staff', 'rental')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class InventoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Inventory model"""
    queryset = Inventory.objects.all().select_related('film', 'store')
    serializer_class = InventorySerializer
    permission_classes = [IsStaffOrAdmin]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get available inventory (not currently rented)"""
        # Find inventory that's either never rented or has been returned
        rented_inventory_ids = Rental.objects.filter(
            return_date__isnull=True
        ).values_list('inventory_id', flat=True)
        
        available = self.queryset.exclude(inventory_id__in=rented_inventory_ids)
        
        page = self.paginate_queryset(available)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)


class RentalViewSet(viewsets.ModelViewSet):
    """ViewSet for Rental model"""
    queryset = Rental.objects.all().select_related(
        'inventory__film', 'customer', 'staff'
    )
    serializer_class = RentalSerializer
    permission_classes = [IsStaffOrAdmin]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active rentals (not yet returned)"""
        active_rentals = self.queryset.filter(return_date__isnull=True)
        
        page = self.paginate_queryset(active_rentals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(active_rentals, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def return_rental(self, request, pk=None):
        """Mark a rental as returned"""
        rental = self.get_object()
        if rental.return_date:
            return Response(
                {'error': 'Rental already returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.utils import timezone
        rental.return_date = timezone.now()
        rental.save()
        
        serializer = self.get_serializer(rental)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment model"""
    queryset = Payment.objects.all().select_related('customer', 'staff', 'rental')
    serializer_class = PaymentSerializer
    permission_classes = [IsStaffOrAdmin]

