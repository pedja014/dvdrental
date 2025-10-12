from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Actor, Category, Country, City, Address, Language,
    Film, FilmActor, FilmCategory, Store, Staff, Customer,
    Inventory, Rental, Payment
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser"""
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['actor_id', 'first_name', 'last_name', 'last_update']
    search_fields = ['first_name', 'last_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name', 'last_update']
    search_fields = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_id', 'country', 'last_update']
    search_fields = ['country']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_id', 'city', 'country', 'last_update']
    search_fields = ['city']
    list_filter = ['country']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['address_id', 'address', 'district', 'city', 'phone']
    search_fields = ['address', 'district']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['language_id', 'name', 'last_update']
    search_fields = ['name']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['film_id', 'title', 'release_year', 'language', 'rental_rate', 'rating']
    search_fields = ['title', 'description']
    list_filter = ['language', 'rating', 'release_year']


@admin.register(FilmActor)
class FilmActorAdmin(admin.ModelAdmin):
    list_display = ['actor', 'film', 'last_update']
    search_fields = ['actor__first_name', 'actor__last_name', 'film__title']


@admin.register(FilmCategory)
class FilmCategoryAdmin(admin.ModelAdmin):
    list_display = ['film', 'category', 'last_update']
    search_fields = ['film__title', 'category__name']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id', 'manager_staff_id', 'address', 'last_update']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'first_name', 'last_name', 'email', 'store', 'active']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['active', 'store']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'first_name', 'last_name', 'email', 'store', 'activebool']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['activebool', 'store']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['inventory_id', 'film', 'store', 'last_update']
    search_fields = ['film__title']
    list_filter = ['store']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['rental_id', 'customer', 'inventory', 'rental_date', 'return_date', 'staff']
    search_fields = ['customer__first_name', 'customer__last_name']
    list_filter = ['rental_date', 'return_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'customer', 'amount', 'payment_date', 'staff']
    search_fields = ['customer__first_name', 'customer__last_name']
    list_filter = ['payment_date']

