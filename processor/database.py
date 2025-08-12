"""
Database utilities for managing items in PostgreSQL database.

Exports:
    - get_all_items():       Returns IDs of all items in the table.
"""

import os

import sqlalchemy

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

engine = sqlalchemy.create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)


def get_all_items():
    """Retrieve all item IDs from the 'items' table in the database."""
    with engine.connect() as connection:
        return connection.execute(sqlalchemy.text("SELECT * FROM repos"))
