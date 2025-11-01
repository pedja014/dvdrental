"""
Database utilities for accessing dvdrental_sample database.
"""
from django.db import connections


def get_dvdrental_connection():
    """Get database connection for dvdrental_sample database"""
    return connections['dvdrental_sample']

