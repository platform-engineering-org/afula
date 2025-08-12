"""
Unit tests for the database module.

Tests:
    - get_all_items() calls the correct SQL query and returns the result.
"""

from unittest import mock

import sqlalchemy
from processor import database


def test_get_all_items_executes_query():
    """Test that get_all_items() executes the expected SQL query."""
    mock_connection = mock.MagicMock()
    mock_execute_result = mock.MagicMock()
    mock_connection.execute.return_value = mock_execute_result

    # Patch the engine.connect() context manager
    with mock.patch.object(database.engine, "connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_connection

        result = database.get_all_items()

        mock_connect.assert_called_once()
        mock_connection.execute.assert_called_once()

        # Extract the SQL text passed to execute
        called_query = mock_connection.execute.call_args[0][0]
        assert isinstance(called_query, sqlalchemy.sql.elements.TextClause)
        assert "SELECT * FROM repos" in str(called_query)

        # The function should return what execute() returns
        assert result == mock_execute_result
