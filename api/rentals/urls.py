"""
Rental domain URLs.
"""
from django.urls import path
from api.rentals.apis import RentalListApi, RentalDetailApi

urlpatterns = [
    path('', RentalListApi.as_view(), name='rental-list'),
    path('<int:rental_id>/', RentalDetailApi.as_view(), name='rental-detail'),
]

