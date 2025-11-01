"""
Film domain serializers.
"""
from rest_framework import serializers


class FilmListOutputSerializer(serializers.Serializer):
    """Serializer for film list response"""
    film_id = serializers.IntegerField()
    title = serializers.CharField()
    release_year = serializers.IntegerField(allow_null=True)
    rating = serializers.CharField(allow_null=True)
    rental_rate = serializers.DecimalField(max_digits=5, decimal_places=2)


class FilmDetailOutputSerializer(serializers.Serializer):
    """Serializer for film detail response"""
    film_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    release_year = serializers.IntegerField(allow_null=True)
    language_id = serializers.IntegerField()
    rental_duration = serializers.IntegerField()
    rental_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    length = serializers.IntegerField(allow_null=True)
    replacement_cost = serializers.DecimalField(max_digits=5, decimal_places=2)
    rating = serializers.CharField(allow_null=True)
    last_update = serializers.DateTimeField()


class FilmCreateInputSerializer(serializers.Serializer):
    """Serializer for creating a film"""
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    release_year = serializers.IntegerField(allow_null=True, required=False)
    language_id = serializers.IntegerField(required=True)
    rental_duration = serializers.IntegerField(min_value=1, required=True)
    rental_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=True)
    length = serializers.IntegerField(allow_null=True, min_value=0, required=False)
    replacement_cost = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=True)
    rating = serializers.ChoiceField(
        choices=['G', 'PG', 'PG-13', 'R', 'NC-17'],
        default='G',
        required=False
    )


class FilmUpdateInputSerializer(serializers.Serializer):
    """Serializer for updating a film"""
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    release_year = serializers.IntegerField(allow_null=True, required=False)
    language_id = serializers.IntegerField(required=False)
    rental_duration = serializers.IntegerField(min_value=1, required=False)
    rental_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=False)
    length = serializers.IntegerField(allow_null=True, min_value=0, required=False)
    replacement_cost = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, required=False)
    rating = serializers.ChoiceField(
        choices=['G', 'PG', 'PG-13', 'R', 'NC-17'],
        required=False
    )

