"""
Register module for managing user and service registration.

This module provides functions and classes to handle the registration
of repositories with Renovate, service initialization, and storing
related metadata in the backend database.

Author: Liora Milbaum
"""

import flask_wtf
import wtforms
import wtforms.validators


class RegisterForm(flask_wtf.FlaskForm):
    """
    Form for registering a new repository.

    This form captures necessary input fields such as repository name,
    Git URL, and metadata for onboarding into the Renovate management system.
    It includes validation methods to ensure input correctness.
    """

    repo_name = wtforms.StringField(
        "Repo Name",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=20),
            wtforms.validators.Regexp(
                r"^[a-zA-Z0-9\-]+$",
                message="Only letters, numbers and dashes are allowed",
            ),
        ],
    )
    repo_url = wtforms.StringField(
        "Repo Url",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=50),
            wtforms.validators.Regexp(
                r"(?:https?|git)://(?:www\.)?(github\.com|gitlab\.com)/([\w.-]+/[\w.-]+)(?:\.git)?",
                message="Git repository URLs from GitHub or GitLab",
            ),
        ],
    )
