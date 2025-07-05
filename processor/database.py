"""
Database utilities for managing items in PostgreSQL database.

Exports:
    - get_all_items():       Returns IDs of all items in the table.
"""

import os

import psycopg2

DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")
DB_NAME = os.environ.get("POSTGRES_DB", "mydb")
DB_USER = os.environ.get("POSTGRES_USER", "myuser")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "mypassword")


def get_all_items():
    """Retrieve all item IDs from the 'items' table in the database."""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cur = conn.cursor()
    cur.execute("SELECT id FROM items WHERE processed = false")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]
