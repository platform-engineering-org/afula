"""
Renovate Repo Manager Microservice.

This microservice provides CRUD operations and automation for managing
software repositories that are monitored and updated by Renovate.

Features:
- Track and manage repositories configured with Renovate.
- Provide APIs to register, update, and remove repositories.
- Support querying the state of dependency update automation.
- Integrate with Git hosting services (e.g., GitHub, GitLab).
- Facilitate visibility and reporting of Renovate activity.

Intended to be used as part of a larger system that automates dependency
management across multiple projects and teams.

Author: Liora Milbaum
"""

import flask

from . import config, database, routes


def create_app(test_config=None):
    """Create and configure the Flask application."""
    myapp = flask.Flask(__name__)

    myapp.config.from_object(config.Config)
    if test_config:
        myapp.config.update(test_config)

    database.db.init_app(myapp)

    @app.route("/")
    def home():
        """Non-blueprint home route."""
        return flask.jsonify(message="Welcome to the Afula app!")

    myapp.register_blueprint(routes.bp)

    with myapp.app_context():
        database.db.create_all()

    return myapp


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
