from django.contrib.auth.models import AbstractUser
from django.db import models


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
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# DVD Rental Database Models (generated from inspectdb and cleaned up)

class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'actor'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'category'
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'country'
        ordering = ['country']

    def __str__(self):
        return self.country


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'city'
        ordering = ['city']

    def __str__(self):
        return self.city


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'address'

    def __str__(self):
        return self.address


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'language'
        ordering = ['name']

    def __str__(self):
        return self.name


class Film(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    original_language = models.ForeignKey(
        Language, on_delete=models.DO_NOTHING, 
        related_name='original_language_films',
        blank=True, null=True
    )
    rental_duration = models.SmallIntegerField(default=3)
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2, default=4.99)
    length = models.SmallIntegerField(blank=True, null=True)
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2, default=19.99)
    rating = models.CharField(max_length=10, blank=True, null=True)
    special_features = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'film'
        ordering = ['title']

    def __str__(self):
        return self.title


class FilmActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.DO_NOTHING, db_column='actor_id')
    film = models.ForeignKey(Film, on_delete=models.DO_NOTHING, db_column='film_id')
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'film_actor'
        unique_together = (('actor', 'film'),)
        # Composite primary key in database: (actor_id, film_id)


class FilmCategory(models.Model):
    film = models.ForeignKey(Film, on_delete=models.DO_NOTHING, db_column='film_id')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id')
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'film_category'
        unique_together = (('film', 'category'),)
        # Composite primary key in database: (film_id, category_id)


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    manager_staff_id = models.SmallIntegerField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'store'

    def __str__(self):
        return f"Store {self.store_id}"


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=50, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=40, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    picture = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    activebool = models.BooleanField(default=True)
    create_date = models.DateField()
    last_update = models.DateTimeField(auto_now=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    film = models.ForeignKey(Film, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'inventory'

    def __str__(self):
        return f"Inventory {self.inventory_id} - {self.film.title}"


class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    return_date = models.DateTimeField(blank=True, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'rental'
        ordering = ['-rental_date']

    def __str__(self):
        return f"Rental {self.rental_id}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    rental = models.ForeignKey(Rental, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'payment'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.payment_id} - ${self.amount}"

