"""
Provide database models for the application.

Defines the core models used for persisting and querying application data:
- Repo: represents the registered repositories.

Classes:
    Repo: A registered repository

Author: Liora Milbaum
"""

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Repo(db.Model):
    """Registered repository."""

    __tablename__ = "repos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
