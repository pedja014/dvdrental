"""
Film domain services.
"""
from typing import Dict
from django.db import transaction
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError, BusinessLogicError
from api.films.selectors import film_exists, film_get_by_id


@transaction.atomic(using='dvdrental_sample')
def film_create(**film_data) -> Dict:
    """
    Create a new film.
    
    Args:
        **film_data: Film data (title, description, release_year, language_id, etc.)
        
    Returns:
        Created film dictionary
        
    Raises:
        BusinessLogicError: If validation fails
    """
    conn = get_dvdrental_connection()
    
    required_fields = ['title', 'language_id', 'rental_duration', 'rental_rate', 'replacement_cost']
    for field in required_fields:
        if field not in film_data or film_data[field] is None:
            raise BusinessLogicError(f"Field '{field}' is required.")
    
    # Validate rental_duration
    if film_data.get('rental_duration', 0) <= 0:
        raise BusinessLogicError("rental_duration must be greater than 0.")
    
    # Validate rental_rate
    if film_data.get('rental_rate', 0) < 0:
        raise BusinessLogicError("rental_rate must be non-negative.")
    
    # Validate replacement_cost
    if film_data.get('replacement_cost', 0) < 0:
        raise BusinessLogicError("replacement_cost must be non-negative.")
    
    with conn.cursor() as cursor:
        # Insert film
        insert_query = """
            INSERT INTO film (title, description, release_year, language_id, 
                            rental_duration, rental_rate, length, replacement_cost, 
                            rating, last_update)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING film_id, title, description, release_year, language_id, 
                     rental_duration, rental_rate, length, replacement_cost, 
                     rating, last_update
        """
        
        cursor.execute(
            insert_query,
            [
                film_data.get('title'),
                film_data.get('description'),
                film_data.get('release_year'),
                film_data.get('language_id'),
                film_data.get('rental_duration'),
                film_data.get('rental_rate'),
                film_data.get('length'),
                film_data.get('replacement_cost'),
                film_data.get('rating', 'G'),
            ]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def film_update(*, film_id: int, **film_data) -> Dict:
    """
    Update an existing film.
    
    Args:
        film_id: Film ID to update
        **film_data: Fields to update
        
    Returns:
        Updated film dictionary
        
    Raises:
        NotFoundError: If film not found
        BusinessLogicError: If validation fails
    """
    if not film_exists(film_id=film_id):
        raise NotFoundError(f"Film with id {film_id} not found.")
    
    # Validate numeric fields if provided
    if 'rental_duration' in film_data and film_data['rental_duration'] <= 0:
        raise BusinessLogicError("rental_duration must be greater than 0.")
    
    if 'rental_rate' in film_data and film_data['rental_rate'] < 0:
        raise BusinessLogicError("rental_rate must be non-negative.")
    
    if 'replacement_cost' in film_data and film_data['replacement_cost'] < 0:
        raise BusinessLogicError("replacement_cost must be non-negative.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build update query dynamically
        update_fields = []
        values = []
        
        allowed_fields = ['title', 'description', 'release_year', 'language_id', 
                         'rental_duration', 'rental_rate', 'length', 
                         'replacement_cost', 'rating']
        
        for field in allowed_fields:
            if field in film_data:
                update_fields.append(f"{field} = %s")
                values.append(film_data[field])
        
        if not update_fields:
            # No fields to update, return existing film
            return film_get_by_id(film_id=film_id)
        
        update_fields.append("last_update = NOW()")
        values.append(film_id)
        
        update_query = f"""
            UPDATE film 
            SET {', '.join(update_fields)}
            WHERE film_id = %s
            RETURNING film_id, title, description, release_year, language_id, 
                     rental_duration, rental_rate, length, replacement_cost, 
                     rating, last_update
        """
        
        cursor.execute(update_query, values)
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def film_delete(*, film_id: int) -> None:
    """
    Delete a film.
    
    Args:
        film_id: Film ID to delete
        
    Raises:
        NotFoundError: If film not found
    """
    if not film_exists(film_id=film_id):
        raise NotFoundError(f"Film with id {film_id} not found.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM film WHERE film_id = %s", [film_id])

