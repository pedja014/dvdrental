"""
Analytics domain URLs.
"""
from django.urls import path
from api.analytics.apis import MostProfitableCategoriesApi, MostProfitableFilmsApi

urlpatterns = [
    path('most-profitable-categories/', MostProfitableCategoriesApi.as_view(), name='analytics-most-profitable-categories'),
    path('most-profitable-films/', MostProfitableFilmsApi.as_view(), name='analytics-most-profitable-films'),
]

