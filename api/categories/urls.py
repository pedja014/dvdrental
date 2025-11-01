"""
Category domain URLs.
"""
from django.urls import path
from api.categories.apis import CategoryListApi, CategoryDetailApi

urlpatterns = [
    path('', CategoryListApi.as_view(), name='category-list'),
    path('<int:category_id>/', CategoryDetailApi.as_view(), name='category-detail'),
]

