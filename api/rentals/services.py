"""
Rental domain services.
"""
from typing import Dict, Optional
from datetime import datetime
from django.db import transaction
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError, BusinessLogicError
from api.rentals.selectors import rental_exists, rental_get_by_id


def _validate_foreign_keys(customer_id: Optional[int], staff_id: Optional[int], inventory_id: Optional[int]) -> None:
    """
    Validate that foreign key references exist.
    
    Args:
        customer_id: Customer ID to validate
        staff_id: Staff ID to validate
        inventory_id: Inventory ID to validate
        
    Raises:
        BusinessLogicError: If validation fails
    """
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        if customer_id is not None:
            cursor.execute("SELECT 1 FROM customer WHERE customer_id = %s", [customer_id])
            if not cursor.fetchone():
                raise BusinessLogicError(f"Customer with id {customer_id} not found.")
        
        if staff_id is not None:
            cursor.execute("SELECT 1 FROM staff WHERE staff_id = %s", [staff_id])
            if not cursor.fetchone():
                raise BusinessLogicError(f"Staff with id {staff_id} not found.")
        
        if inventory_id is not None:
            cursor.execute("SELECT 1 FROM inventory WHERE inventory_id = %s", [inventory_id])
            if not cursor.fetchone():
                raise BusinessLogicError(f"Inventory with id {inventory_id} not found.")


@transaction.atomic(using='dvdrental_sample')
def rental_create(
    *,
    inventory_id: int,
    customer_id: int,
    staff_id: int,
    rental_date: Optional[datetime] = None,
    return_date: Optional[datetime] = None
) -> Dict:
    """
    Create a new rental.
    
    Args:
        inventory_id: Inventory ID
        customer_id: Customer ID
        staff_id: Staff ID
        rental_date: Optional rental date (defaults to now)
        return_date: Optional return date
        
    Returns:
        Created rental dictionary
        
    Raises:
        BusinessLogicError: If validation fails
    """
    # Validate foreign keys
    _validate_foreign_keys(customer_id, staff_id, inventory_id)
    
    # Check if inventory is available (not already rented)
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Check if there's an active rental for this inventory
        cursor.execute(
            "SELECT 1 FROM rental WHERE inventory_id = %s AND return_date IS NULL",
            [inventory_id]
        )
        if cursor.fetchone():
            raise BusinessLogicError(f"Inventory item {inventory_id} is currently rented.")
    
    if rental_date is None:
        rental_date = datetime.now()
    
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id, last_update) VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update",
            [rental_date, inventory_id, customer_id, return_date, staff_id]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def rental_update(
    *,
    rental_id: int,
    inventory_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    staff_id: Optional[int] = None,
    return_date: Optional[datetime] = None
) -> Dict:
    """
    Update an existing rental.
    
    Args:
        rental_id: Rental ID to update
        inventory_id: Optional new inventory ID
        customer_id: Optional new customer ID
        staff_id: Optional new staff ID
        return_date: Optional return date (to mark as returned)
        
    Returns:
        Updated rental dictionary
        
    Raises:
        NotFoundError: If rental not found
        BusinessLogicError: If validation fails
    """
    if not rental_exists(rental_id=rental_id):
        raise NotFoundError(f"Rental with id {rental_id} not found.")
    
    # Get existing rental to validate foreign keys
    existing = rental_get_by_id(rental_id=rental_id)
    
    final_customer_id = customer_id if customer_id is not None else existing['customer_id']
    final_staff_id = staff_id if staff_id is not None else existing['staff_id']
    final_inventory_id = inventory_id if inventory_id is not None else existing['inventory_id']
    
    # Validate foreign keys if changed
    if customer_id is not None or staff_id is not None or inventory_id is not None:
        _validate_foreign_keys(
            customer_id if customer_id is not None else None,
            staff_id if staff_id is not None else None,
            inventory_id if inventory_id is not None else None
        )
    
    # If changing inventory, check availability
    if inventory_id is not None and inventory_id != existing['inventory_id']:
        conn = get_dvdrental_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM rental WHERE inventory_id = %s AND return_date IS NULL AND rental_id != %s",
                [inventory_id, rental_id]
            )
            if cursor.fetchone():
                raise BusinessLogicError(f"Inventory item {inventory_id} is currently rented.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build update query dynamically
        update_fields = []
        values = []
        
        if inventory_id is not None:
            update_fields.append("inventory_id = %s")
            values.append(inventory_id)
        
        if customer_id is not None:
            update_fields.append("customer_id = %s")
            values.append(customer_id)
        
        if staff_id is not None:
            update_fields.append("staff_id = %s")
            values.append(staff_id)
        
        if return_date is not None:
            update_fields.append("return_date = %s")
            values.append(return_date)
        
        if not update_fields:
            # No fields to update, return existing rental
            return existing
        
        values.append(rental_id)
        
        update_query = f"""
            UPDATE rental 
            SET {', '.join(update_fields)}, last_update = NOW()
            WHERE rental_id = %s
            RETURNING rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
        """
        
        cursor.execute(update_query, values)
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def rental_delete(*, rental_id: int) -> None:
    """
    Delete a rental.
    
    Args:
        rental_id: Rental ID to delete
        
    Raises:
        NotFoundError: If rental not found
    """
    if not rental_exists(rental_id=rental_id):
        raise NotFoundError(f"Rental with id {rental_id} not found.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM rental WHERE rental_id = %s", [rental_id])

