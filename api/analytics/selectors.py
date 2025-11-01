"""
Analytics domain selectors using stored procedures.
"""
from typing import List, Dict, Optional
from api.common.db import get_dvdrental_connection
from api.common.exceptions import BusinessLogicError


def analytics_get_most_profitable_categories(*, year: Optional[int] = None) -> List[Dict]:
    """
    Get most profitable categories by year using stored procedure.
    
    Args:
        year: Optional year filter. If None, returns all years grouped by year.
        
    Returns:
        List of category profitability dictionaries
        
    Raises:
        BusinessLogicError: If stored procedure fails
    """
    conn = get_dvdrental_connection()
    
    try:
        with conn.cursor() as cursor:
            if year is not None:
                cursor.execute(
                    "SELECT * FROM get_most_profitable_categories_by_year(%s)",
                    [year]
                )
            else:
                cursor.execute(
                    "SELECT * FROM get_most_profitable_categories_by_year(NULL)"
                )
            
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
    except Exception as e:
        raise BusinessLogicError(f"Failed to retrieve category profitability data: {str(e)}")


def analytics_get_most_profitable_films(
    *, 
    year: Optional[int] = None,
    limit: int = 100
) -> List[Dict]:
    """
    Get most profitable films by year using stored procedure.
    
    Args:
        year: Optional year filter. If None, returns all years grouped by year.
        limit: Maximum number of results to return (default 100)
        
    Returns:
        List of film profitability dictionaries
        
    Raises:
        BusinessLogicError: If stored procedure fails
    """
    conn = get_dvdrental_connection()
    
    if limit < 1 or limit > 1000:
        raise BusinessLogicError("Limit must be between 1 and 1000")
    
    try:
        with conn.cursor() as cursor:
            if year is not None:
                cursor.execute(
                    "SELECT * FROM get_most_profitable_films_by_year(%s, %s)",
                    [year, limit]
                )
            else:
                cursor.execute(
                    "SELECT * FROM get_most_profitable_films_by_year(NULL, %s)",
                    [limit]
                )
            
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return results
    except Exception as e:
        raise BusinessLogicError(f"Failed to retrieve film profitability data: {str(e)}")

