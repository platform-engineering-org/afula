"""
Register module for managing user and service registration.

This module provides functions and classes to handle the registration
of repositories with Renovate, service initialization, and storing
related metadata in the backend database.

Author: Liora Milbaum
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class RegisterForm(FlaskForm):
    """
    Form for registering a new repository.

    This form captures necessary input fields such as repository name,
    Git URL, and metadata for onboarding into the Renovate management system.
    It includes validation methods to ensure input correctness.
    """

    repo_name = StringField(
        "Repo Name",
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            Regexp(
                r"^[a-zA-Z0-9\-]+$",
                message="Only letters, numbers and dashes are allowed",
            ),
        ],
    )
    repo_url = StringField(
        "Repo Url",
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(
                r"(?:https?|git)://(?:www\.)?(github\.com|gitlab\.com)/([\w.-]+/[\w.-]+)(?:\.git)?",
                message="Git repository URLs from GitHub or GitLab",
            ),
        ],
    )
