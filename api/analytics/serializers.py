"""
Analytics domain serializers.
"""
from rest_framework import serializers


class CategoryProfitOutputSerializer(serializers.Serializer):
    """Serializer for category profitability response"""
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    year = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    rental_count = serializers.IntegerField()
    film_count = serializers.IntegerField()


class FilmProfitOutputSerializer(serializers.Serializer):
    """Serializer for film profitability response"""
    film_id = serializers.IntegerField()
    title = serializers.CharField()
    year = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    rental_count = serializers.IntegerField()
    category_names = serializers.ListField(child=serializers.CharField())

