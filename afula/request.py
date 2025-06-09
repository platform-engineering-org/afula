from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
import re
from wtforms.validators import DataRequired, Length, Regexp


class RequestForm(FlaskForm):
    repo_name = StringField(
        'Repo Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20),
            Regexp(r'^[a-zA-Z0-9\-]+$', message="Only letters, numbers and dashes are allowed")
        ]
    )
    repo_url = StringField(
        'Repo Url',
        validators=[
            DataRequired(),
            Length(min=2, max=50),
            Regexp(r'(?:https?|git)://(?:www\.)?(github\.com|gitlab\.com)/([\w.-]+/[\w.-]+)(?:\.git)?', message="Git repository URLs from GitHub or GitLab")
        ]
    )
