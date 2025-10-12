from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    CustomUser, Actor, Category, Country, City, Address, Language,
    Film, FilmActor, FilmCategory, Store, Staff, Customer, 
    Inventory, Rental, Payment
)


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'role': {'default': 'customer'},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details"""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.country', read_only=True)
    
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.city', read_only=True)
    
    class Meta:
        model = Address
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = Film
        fields = '__all__'


class FilmDetailSerializer(serializers.ModelSerializer):
    """Detailed film serializer with related data"""
    language_name = serializers.CharField(source='language.name', read_only=True)
    actors = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Film
        fields = '__all__'
    
    def get_actors(self, obj):
        film_actors = FilmActor.objects.filter(film=obj).select_related('actor')
        return [{'id': fa.actor.actor_id, 'name': str(fa.actor)} for fa in film_actors]
    
    def get_categories(self, obj):
        film_categories = FilmCategory.objects.filter(film=obj).select_related('category')
        return [{'id': fc.category.category_id, 'name': fc.category.name} for fc in film_categories]


class FilmActorSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.__str__', read_only=True)
    film_title = serializers.CharField(source='film.title', read_only=True)
    
    class Meta:
        model = FilmActor
        fields = '__all__'


class FilmCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    film_title = serializers.CharField(source='film.title', read_only=True)
    
    class Meta:
        model = FilmCategory
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    address_detail = serializers.CharField(source='address.address', read_only=True)
    
    class Meta:
        model = Store
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    address_detail = serializers.CharField(source='address.address', read_only=True)
    store_id_display = serializers.CharField(source='store.store_id', read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {'picture': {'write_only': True}}


class CustomerSerializer(serializers.ModelSerializer):
    address_detail = serializers.CharField(source='address.address', read_only=True)
    store_id_display = serializers.CharField(source='store.store_id', read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    film_title = serializers.CharField(source='film.title', read_only=True)
    store_id_display = serializers.CharField(source='store.store_id', read_only=True)
    
    class Meta:
        model = Inventory
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.__str__', read_only=True)
    staff_name = serializers.CharField(source='staff.__str__', read_only=True)
    film_title = serializers.CharField(source='inventory.film.title', read_only=True)
    
    class Meta:
        model = Rental
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.__str__', read_only=True)
    staff_name = serializers.CharField(source='staff.__str__', read_only=True)
    rental_id_display = serializers.IntegerField(source='rental.rental_id', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'

