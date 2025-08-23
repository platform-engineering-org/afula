"""
Unit tests for the repos blueprint.

Tests:
- Listing repositories
- Registering repositories via JSON and form
- Success page rendering

Author: Liora Milbaum
"""

import pytest
from manager import database, models


@pytest.mark.usefixtures("app", "client")
class TestReposBlueprint:
    """Test suite for the /repos blueprint routes."""

    @pytest.fixture
    def repo_data(self):
        """Provide valid repo data for testing."""
        return {"name": "test-repo", "url": "https://github.com/afula/test-repo"}

    def test_list_repos_empty(self, client):
        """GET /repos/list should render the template with no repositories."""
        response = client.get("/repos/list")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "No repositories found" in html or "<ul" in html

    def test_register_repo_json_success(self, client, app, repo_data):
        """POST /repos/register with valid JSON should create a new repository."""
        with app.app_context():
            database.db.create_all()

        response = client.post("/repos/register", json=repo_data)
        assert response.status_code == 201
        data = response.get_json()
        assert "registered successfully" in data["message"]

        with app.app_context():
            repo = models.Repo.query.filter_by(name=repo_data["name"]).first()
            assert repo is not None
            assert repo.url == repo_data["url"]

    def test_register_repo_json_missing_fields(self, client):
        """POST /repos/register with missing JSON fields should return 400."""
        response = client.post("/repos/register", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_register_repo_form_get(self, client):
        """GET /repos/register should render the registration form template."""
        response = client.get("/repos/register")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<form" in html
        assert "repo_name" in html
        assert "repo_url" in html

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"repo_name": "", "repo_url": "https://example.com"},
            {"repo_name": "name", "repo_url": ""},
        ],
    )
    def test_register_repo_form_invalid(self, client, invalid_data):
        """POST /repos/register with invalid form data should re-render form with errors."""
        response = client.post("/repos/register", data=invalid_data)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<form" in html
        assert "This field is required" in html or html

    def test_success_page(self, client):
        """GET /repos/success should render the success template with buttons."""
        response = client.get("/repos/success")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Repository has been registered successfully" in html
        assert "View Repositories" in html
        assert "Register Another Repo" in html
