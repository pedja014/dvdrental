"""
Rental domain serializers.
"""
from rest_framework import serializers


class RentalListOutputSerializer(serializers.Serializer):
    """Serializer for rental list response"""
    rental_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    rental_date = serializers.DateTimeField()
    return_date = serializers.DateTimeField(allow_null=True)


class RentalDetailOutputSerializer(serializers.Serializer):
    """Serializer for rental detail response"""
    rental_id = serializers.IntegerField()
    rental_date = serializers.DateTimeField()
    inventory_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    return_date = serializers.DateTimeField(allow_null=True)
    staff_id = serializers.IntegerField()
    last_update = serializers.DateTimeField()


class RentalCreateInputSerializer(serializers.Serializer):
    """Serializer for creating a rental"""
    inventory_id = serializers.IntegerField(required=True)
    customer_id = serializers.IntegerField(required=True)
    staff_id = serializers.IntegerField(required=True)
    rental_date = serializers.DateTimeField(required=False)
    return_date = serializers.DateTimeField(allow_null=True, required=False)


class RentalUpdateInputSerializer(serializers.Serializer):
    """Serializer for updating a rental"""
    inventory_id = serializers.IntegerField(required=False)
    customer_id = serializers.IntegerField(required=False)
    staff_id = serializers.IntegerField(required=False)
    return_date = serializers.DateTimeField(allow_null=True, required=False)

