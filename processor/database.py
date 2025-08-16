"""
Database utilities for managing items in PostgreSQL database.

Exports:
    - get_all_items():       Returns IDs of all items in the table.
"""

import sqlalchemy
from db.config import get_postgres_uri

engine = sqlalchemy.create_engine(get_postgres_uri())


def get_all_items():
    """Retrieve all item IDs from the 'items' table in the database."""
    with engine.connect() as connection:
        return connection.execute(sqlalchemy.text("SELECT * FROM repos"))
