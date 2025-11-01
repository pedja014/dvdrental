"""
Category domain services.
"""
from typing import Dict
from django.db import transaction
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError, BusinessLogicError
from api.categories.selectors import category_exists, category_get_by_id, category_exists_by_name


@transaction.atomic(using='dvdrental_sample')
def category_create(*, name: str) -> Dict:
    """
    Create a new category.
    
    Args:
        name: Category name
        
    Returns:
        Created category dictionary
        
    Raises:
        BusinessLogicError: If validation fails
    """
    if not name or not name.strip():
        raise BusinessLogicError("Category name is required.")
    
    if category_exists_by_name(name=name.strip()):
        raise BusinessLogicError(f"Category with name '{name}' already exists.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO category (name, last_update) VALUES (%s, NOW()) RETURNING category_id, name, last_update",
            [name.strip()]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def category_update(*, category_id: int, name: str) -> Dict:
    """
    Update an existing category.
    
    Args:
        category_id: Category ID to update
        name: New category name
        
    Returns:
        Updated category dictionary
        
    Raises:
        NotFoundError: If category not found
        BusinessLogicError: If validation fails
    """
    if not category_exists(category_id=category_id):
        raise NotFoundError(f"Category with id {category_id} not found.")
    
    if not name or not name.strip():
        raise BusinessLogicError("Category name is required.")
    
    # Check if another category with this name exists
    existing = category_get_by_id(category_id=category_id)
    if existing['name'] != name.strip() and category_exists_by_name(name=name.strip()):
        raise BusinessLogicError(f"Category with name '{name}' already exists.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE category SET name = %s, last_update = NOW() WHERE category_id = %s RETURNING category_id, name, last_update",
            [name.strip(), category_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def category_delete(*, category_id: int) -> None:
    """
    Delete a category.
    
    Args:
        category_id: Category ID to delete
        
    Raises:
        NotFoundError: If category not found
    """
    if not category_exists(category_id=category_id):
        raise NotFoundError(f"Category with id {category_id} not found.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM category WHERE category_id = %s", [category_id])

