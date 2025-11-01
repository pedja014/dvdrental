"""
Payment domain selectors using raw SQL queries.
"""
from typing import List, Dict, Optional, Tuple
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError


def payment_list(
    *,
    customer_id: Optional[int] = None,
    staff_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0
) -> Tuple[List[Dict], int]:
    """
    List payments with pagination and optional filtering.
    
    Args:
        customer_id: Optional filter by customer ID
        staff_id: Optional filter by staff ID
        limit: Number of records to return
        offset: Number of records to skip
        
    Returns:
        Tuple of (payment list, total count)
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build query with optional filters
        base_query = "SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date FROM payment"
        count_query = "SELECT COUNT(*) FROM payment"
        
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
        base_query += " ORDER BY payment_date DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(base_query, params)
        
        columns = [col[0] for col in cursor.description]
        payments = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return payments, total_count


def payment_get_by_id(*, payment_id: int) -> Dict:
    """
    Get a single payment by ID.
    
    Args:
        payment_id: Payment ID to retrieve
        
    Returns:
        Payment dictionary
        
    Raises:
        NotFoundError: If payment not found
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date FROM payment WHERE payment_id = %s",
            [payment_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            raise NotFoundError(f"Payment with id {payment_id} not found.")
        
        return dict(zip(columns, row))


def payment_exists(*, payment_id: int) -> bool:
    """
    Check if a payment exists.
    
    Args:
        payment_id: Payment ID to check
        
    Returns:
        True if payment exists, False otherwise
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM payment WHERE payment_id = %s", [payment_id])
        return cursor.fetchone() is not None

