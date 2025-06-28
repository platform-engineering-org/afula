"""
Provide and configure the SQLAlchemy database extension.

This module initializes the global `db` instance using Flask‑SQLAlchemy.

Author: Liora Milbaum
"""

import os

import flask_sqlalchemy
import sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()
DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")
DB_NAME = os.environ.get("POSTGRES_DB", "mydb")
DB_USER = os.environ.get("POSTGRES_USER", "myuser")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "mypassword")

engine = sqlalchemy.create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}", echo=True
)


def init_db():
    """Initialize DB."""
    sqlalchemy.Base.metadata.create_all(engine)
