"""
Payment domain services.
"""
from typing import Dict, Optional
from datetime import datetime
from django.db import transaction
from api.common.db import get_dvdrental_connection
from api.common.exceptions import NotFoundError, BusinessLogicError
from api.payments.selectors import payment_exists, payment_get_by_id


def _validate_foreign_keys(customer_id: Optional[int], staff_id: Optional[int], rental_id: Optional[int]) -> None:
    """
    Validate that foreign key references exist.
    
    Args:
        customer_id: Customer ID to validate
        staff_id: Staff ID to validate
        rental_id: Rental ID to validate
        
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
        
        if rental_id is not None:
            cursor.execute("SELECT 1 FROM rental WHERE rental_id = %s", [rental_id])
            if not cursor.fetchone():
                raise BusinessLogicError(f"Rental with id {rental_id} not found.")


@transaction.atomic(using='dvdrental_sample')
def payment_create(
    *,
    customer_id: int,
    staff_id: int,
    amount: float,
    rental_id: Optional[int] = None,
    payment_date: Optional[datetime] = None
) -> Dict:
    """
    Create a new payment.
    
    Args:
        customer_id: Customer ID
        staff_id: Staff ID
        amount: Payment amount
        rental_id: Optional rental ID
        payment_date: Optional payment date (defaults to now)
        
    Returns:
        Created payment dictionary
        
    Raises:
        BusinessLogicError: If validation fails
    """
    if amount <= 0:
        raise BusinessLogicError("Payment amount must be greater than 0.")
    
    # Validate foreign keys
    _validate_foreign_keys(customer_id, staff_id, rental_id)
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        if payment_date is None:
            payment_date = datetime.now()
        
        cursor.execute(
            "INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES (%s, %s, %s, %s, %s) RETURNING payment_id, customer_id, staff_id, rental_id, amount, payment_date",
            [customer_id, staff_id, rental_id, amount, payment_date]
        )
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def payment_update(
    *,
    payment_id: int,
    customer_id: Optional[int] = None,
    staff_id: Optional[int] = None,
    rental_id: Optional[int] = None,
    amount: Optional[float] = None
) -> Dict:
    """
    Update an existing payment.
    
    Args:
        payment_id: Payment ID to update
        customer_id: Optional new customer ID
        staff_id: Optional new staff ID
        rental_id: Optional new rental ID
        amount: Optional new amount
        
    Returns:
        Updated payment dictionary
        
    Raises:
        NotFoundError: If payment not found
        BusinessLogicError: If validation fails
    """
    if not payment_exists(payment_id=payment_id):
        raise NotFoundError(f"Payment with id {payment_id} not found.")
    
    if amount is not None and amount <= 0:
        raise BusinessLogicError("Payment amount must be greater than 0.")
    
    # Get existing payment to validate foreign keys
    existing = payment_get_by_id(payment_id=payment_id)
    
    final_customer_id = customer_id if customer_id is not None else existing['customer_id']
    final_staff_id = staff_id if staff_id is not None else existing['staff_id']
    final_rental_id = rental_id if rental_id is not None else existing['rental_id']
    
    # Validate foreign keys if changed
    if customer_id is not None or staff_id is not None or rental_id is not None:
        _validate_foreign_keys(
            customer_id if customer_id is not None else None,
            staff_id if staff_id is not None else None,
            rental_id if rental_id is not None else None
        )
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        # Build update query dynamically
        update_fields = []
        values = []
        
        if customer_id is not None:
            update_fields.append("customer_id = %s")
            values.append(customer_id)
        
        if staff_id is not None:
            update_fields.append("staff_id = %s")
            values.append(staff_id)
        
        if rental_id is not None:
            update_fields.append("rental_id = %s")
            values.append(rental_id)
        
        if amount is not None:
            update_fields.append("amount = %s")
            values.append(amount)
        
        if not update_fields:
            # No fields to update, return existing payment
            return existing
        
        values.append(payment_id)
        
        update_query = f"""
            UPDATE payment 
            SET {', '.join(update_fields)}
            WHERE payment_id = %s
            RETURNING payment_id, customer_id, staff_id, rental_id, amount, payment_date
        """
        
        cursor.execute(update_query, values)
        
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        
        return dict(zip(columns, row))


@transaction.atomic(using='dvdrental_sample')
def payment_delete(*, payment_id: int) -> None:
    """
    Delete a payment.
    
    Args:
        payment_id: Payment ID to delete
        
    Raises:
        NotFoundError: If payment not found
    """
    if not payment_exists(payment_id=payment_id):
        raise NotFoundError(f"Payment with id {payment_id} not found.")
    
    conn = get_dvdrental_connection()
    
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM payment WHERE payment_id = %s", [payment_id])

