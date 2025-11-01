"""
Payment domain serializers.
"""
from rest_framework import serializers


class PaymentListOutputSerializer(serializers.Serializer):
    """Serializer for payment list response"""
    payment_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    payment_date = serializers.DateTimeField()


class PaymentDetailOutputSerializer(serializers.Serializer):
    """Serializer for payment detail response"""
    payment_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    staff_id = serializers.IntegerField()
    rental_id = serializers.IntegerField(allow_null=True)
    amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    payment_date = serializers.DateTimeField()


class PaymentCreateInputSerializer(serializers.Serializer):
    """Serializer for creating a payment"""
    customer_id = serializers.IntegerField(required=True)
    staff_id = serializers.IntegerField(required=True)
    rental_id = serializers.IntegerField(allow_null=True, required=False)
    amount = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0.01, required=True)
    payment_date = serializers.DateTimeField(required=False)


class PaymentUpdateInputSerializer(serializers.Serializer):
    """Serializer for updating a payment"""
    customer_id = serializers.IntegerField(required=False)
    staff_id = serializers.IntegerField(required=False)
    rental_id = serializers.IntegerField(allow_null=True, required=False)
    amount = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0.01, required=False)

