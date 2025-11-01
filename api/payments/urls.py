"""
Payment domain URLs.
"""
from django.urls import path
from api.payments.apis import PaymentListApi, PaymentDetailApi

urlpatterns = [
    path('', PaymentListApi.as_view(), name='payment-list'),
    path('<int:payment_id>/', PaymentDetailApi.as_view(), name='payment-detail'),
]

