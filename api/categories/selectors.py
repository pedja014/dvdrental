"""
Category domain selectors using raw SQL queries.
"""
from typing import List, Dict, Optional, Tuple
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError


def category_list(
    *,
    limit: int = 20,
    offset: int = 0
) -> Tuple[List[Dict], int]:
    """
    List all categories with pagination.
    
    Args:
        limit: Number of records to return
        offset: Number of records to skip
        
    Returns:
        Tuple of (category list, total count)
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM category")
        total_count = cursor.fetchone()[0]
        
        # Get paginated results
        cursor.execute(
            "SELECT category_id, name, last_update FROM category ORDER BY name LIMIT %s OFFSET %s",
            [limit, offset]
        )
        
        columns = [col[0] for col in cursor.description]
        categories = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return categories, total_count


def category_get_by_id(*, category_id: int) -> Dict:
    """
    Get a single category by ID.
    
    Args:
        category_id: Category ID to retrieve
        
    Returns:
        Category dictionary
        
    Raises:
        NotFoundError: If category not found
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT category_id, name, last_update FROM category WHERE category_id = %s",
            [category_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            raise NotFoundError(f"Category with id {category_id} not found.")
        
        return dict(zip(columns, row))


def category_exists(*, category_id: int) -> bool:
    """
    Check if a category exists.
    
    Args:
        category_id: Category ID to check
        
    Returns:
        True if category exists, False otherwise
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM category WHERE category_id = %s", [category_id])
        return cursor.fetchone() is not None


def category_exists_by_name(*, name: str) -> bool:
    """
    Check if a category with the given name already exists.
    
    Args:
        name: Category name to check
        
    Returns:
        True if category exists, False otherwise
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM category WHERE name = %s", [name])
        return cursor.fetchone() is not None

