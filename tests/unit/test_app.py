"""
Unit tests for the Flask application factory and /register endpoint.

This module tests:
- The creation and configuration of the Flask app via create_app().
- That the /register route is properly registered.
- That posting valid data to /register inserts a Repo into the database.
- That invalid payloads return appropriate error responses.
"""

import pytest

from afula import Repo, application, database


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    myapp = application.create_app(test_config=test_config)

    with myapp.app_context():
        database.db.init_app(myapp)
        database.db.create_all()
        yield myapp


@pytest.fixture
def client(app):
    """
    Provide a test client for the Flask app.

    Allows sending HTTP requests to the application
    without running a real server.
    """
    return app.test_client()


def test_register_endpoint_exists(app):
    """Make sure /register URL is registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/register" in rules


def test_register_repo_success(client, app):
    """POST /register should insert a new Repo record into the DB."""
    payload = {"name": "test-repo", "url": "https://example.com"}
    response = client.post("/register", json=payload)
    assert response.status_code == 201

    # Verify the repo exists in the DB
    with app.app_context():
        repo = Repo.query.filter_by(name="test-repo").first()
        assert repo is not None
        assert repo.url == "https://example.com"


def test_register_repo_bad_payload(client):
    """POST /register with missing fields should return 400."""
    response = client.post("/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
