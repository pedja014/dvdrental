"""
Category domain serializers.
"""
from rest_framework import serializers


class CategoryOutputSerializer(serializers.Serializer):
    """Serializer for category output"""
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    last_update = serializers.DateTimeField()


class CategoryCreateInputSerializer(serializers.Serializer):
    """Serializer for creating a category"""
    name = serializers.CharField(max_length=25, required=True)


class CategoryUpdateInputSerializer(serializers.Serializer):
    """Serializer for updating a category"""
    name = serializers.CharField(max_length=25, required=True)

