"""
Unit tests for the database utilities module.

Verifies the behavior of functions that interact with the database,
including retrieving all items. Uses an in-memory SQLite database
for isolated testing to avoid dependence on a real PostgreSQL instance.

Uses pytest for test organization.
"""

import pytest
import sqlalchemy
from processor import database


@pytest.fixture
def in_memory_engine(monkeypatch):
    """Replace the engine with an in-memory SQLite engine for testing."""
    engine = sqlalchemy.create_engine("sqlite:///:memory:")
    monkeypatch.setattr(database, "engine", engine)
    return engine


@pytest.fixture
def create_test_table(in_memory_engine):
    """Create a temporary 'repos' table in the in-memory database."""
    metadata = sqlalchemy.MetaData()
    repos = sqlalchemy.Table(
        "repos",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    )
    metadata.create_all(in_memory_engine)
    return repos


def test_get_all_items_empty(in_memory_engine, create_test_table):
    """Test that get_all_items returns empty list when table has no rows."""
    result = list(database.get_all_items())
    assert result == []


def test_get_all_items_with_data(in_memory_engine, create_test_table):
    """Test that get_all_items returns rows correctly when table has data."""
    with in_memory_engine.connect() as conn:
        conn.execute(sqlalchemy.text("INSERT INTO repos (id) VALUES (1)"))
        conn.execute(sqlalchemy.text("INSERT INTO repos (id) VALUES (2)"))
        conn.commit()

    rows = list(database.get_all_items())
    # SQLAlchemy Row objects may be tuples or RowProxy; convert to IDs
    ids = [row[0] for row in rows]
    assert ids == [1, 2]
