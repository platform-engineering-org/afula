"""
Provide and configure the SQLAlchemy database extension.

This module initializes the global `db` instance using Flask‑SQLAlchemy.

Author: Liora Milbaum
"""

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()
