"""
Film domain selectors using raw SQL queries.
"""
from typing import List, Dict, Optional, Tuple
from django.db import connection
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError


def film_list(
    *,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Tuple[List[Dict], int]:
    """
    List films with pagination and optional search.
    
    Args:
        search: Optional search term for title or description
        limit: Number of records to return
        offset: Number of records to skip
        
    Returns:
        Tuple of (film list, total count)
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build query with optional search
        base_query = "SELECT film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update FROM film"
        count_query = "SELECT COUNT(*) FROM film"
        
        params = []
        conditions = []
        
        if search:
            conditions.append("(title ILIKE %s OR description ILIKE %s)")
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern])
        
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Get total count
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Get paginated results
        base_query += " ORDER BY title LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(base_query, params)
        
        columns = [col[0] for col in cursor.description]
        films = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return films, total_count


def film_get_by_id(*, film_id: int) -> Dict:
    """
    Get a single film by ID.
    
    Args:
        film_id: Film ID to retrieve
        
    Returns:
        Film dictionary
        
    Raises:
        NotFoundError: If film not found
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT film_id, title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating, last_update FROM film WHERE film_id = %s",
            [film_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            raise NotFoundError(f"Film with id {film_id} not found.")
        
        return dict(zip(columns, row))


def film_exists(*, film_id: int) -> bool:
    """
    Check if a film exists.
    
    Args:
        film_id: Film ID to check
        
    Returns:
        True if film exists, False otherwise
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM film WHERE film_id = %s", [film_id])
        return cursor.fetchone() is not None


def film_get_special_features(*, film_id: int) -> List[str]:
    """
    Get special features for a film (stored as PostgreSQL array).
    
    Args:
        film_id: Film ID
        
    Returns:
        List of special features
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT special_features FROM film WHERE film_id = %s", [film_id])
        row = cursor.fetchone()
        
        if not row or not row[0]:
            return []
        
        return row[0] if isinstance(row[0], list) else []

