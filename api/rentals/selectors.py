"""
Rental domain selectors using raw SQL queries.
"""
from typing import List, Dict, Optional, Tuple
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError


def rental_list(
    *,
    customer_id: Optional[int] = None,
    staff_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0
) -> Tuple[List[Dict], int]:
    """
    List rentals with pagination and optional filtering.
    
    Args:
        customer_id: Optional filter by customer ID
        staff_id: Optional filter by staff ID
        limit: Number of records to return
        offset: Number of records to skip
        
    Returns:
        Tuple of (rental list, total count)
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build query with optional filters
        base_query = "SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update FROM rental"
        count_query = "SELECT COUNT(*) FROM rental"
        
        params = []
        conditions = []
        
        if customer_id is not None:
            conditions.append("customer_id = %s")
            params.append(customer_id)
        
        if staff_id is not None:
            conditions.append("staff_id = %s")
            params.append(staff_id)
        
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
            base_query += where_clause
            count_query += where_clause
        
        # Get total count
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Get paginated results
        base_query += " ORDER BY rental_date DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(base_query, params)
        
        columns = [col[0] for col in cursor.description]
        rentals = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return rentals, total_count


def rental_get_by_id(*, rental_id: int) -> Dict:
    """
    Get a single rental by ID.
    
    Args:
        rental_id: Rental ID to retrieve
        
    Returns:
        Rental dictionary
        
    Raises:
        NotFoundError: If rental not found
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update FROM rental WHERE rental_id = %s",
            [rental_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            raise NotFoundError(f"Rental with id {rental_id} not found.")
        
        return dict(zip(columns, row))


def rental_exists(*, rental_id: int) -> bool:
    """
    Check if a rental exists.
    
    Args:
        rental_id: Rental ID to check
        
    Returns:
        True if rental exists, False otherwise
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM rental WHERE rental_id = %s", [rental_id])
        return cursor.fetchone() is not None

