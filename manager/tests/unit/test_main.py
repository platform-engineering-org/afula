"""
Unit tests for the Flask application factory and /register endpoint.

This module tests:
- App creates with default config.
- App uses provided test config.
- Routes register correctly.

Author: Liora Milbaum
"""

from unittest import mock

from manager import main


def test_create_app_default():
    """App should load default config if test_config not provided."""
    with (
        mock.patch("manager.database.db.init_app") as mock_init,
        mock.patch("manager.database.db.create_all") as mock_create_all,
    ):
        app = main.create_app()

        mock_init.assert_called_once_with(app)
        mock_create_all.assert_called_once()

        assert "SQLALCHEMY_DATABASE_URI" in app.config


def test_create_app_with_test_config():
    """App should use given test_config."""
    with (
        mock.patch("manager.database.db.init_app") as mock_init,
        mock.patch("manager.database.db.create_all") as mock_create_all,
    ):

        class TestConfig:
            """Configuration for tests. Uses in-memory SQLite and disables tracking."""

            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            TESTING = True

        app = main.create_app(test_config=TestConfig)

        mock_init.assert_called_once_with(app)
        mock_create_all.assert_called_once()

        assert app.config["TESTING"] is True
        assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_home_route(client):
    """GET / should return welcome JSON."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["message"] == "Welcome to the Afula app!"


def test_register_endpoint_exists(app):
    """Make sure /repos/register URL is registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/repos/register" in rules


def test_register_repo_success(client, app):
    """POST /repos/register should insert a new Repo record into the DB."""
    with app.app_context():
        main.database.db.create_all()

    payload = {"name": "test-repo", "url": "https://github.com/afula/test-repo"}
    response = client.post("/repos/register", json=payload)

    assert response.status_code == 201


def test_register_repo_bad_payload(client):
    """POST /repos/register with missing fields should return 400."""
    response = client.post("/repos/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
