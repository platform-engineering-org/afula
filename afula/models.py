"""
Provide database models for the application.

Defines the core models used for persisting and querying application data:
- Repo: represents the registered repositories.

Classes:
    Repo: A registered repository

Author: Liora Milbaum
"""

import database


class Repo(database.db.Model):
    """Registered repository."""

    __tablename__ = "repos"

    id = database.db.Column(database.db.Integer, primary_key=True)
    name = database.db.Column(database.db.String(128), nullable=False)
    url = database.db.Column(database.db.String(256), nullable=False, unique=True)
    active = database.db.Column(database.db.Boolean, default=True)
