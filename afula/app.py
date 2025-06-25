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

import configparser
import os

import flask

import database
import routes


def create_app():
    """Create and configure the Flask application."""
    DB_HOST = os.environ.get("POSTGRES_HOST", "postgres")
    DB_NAME = os.environ.get("POSTGRES_DB", "mydb")
    DB_USER = os.environ.get("POSTGRES_USER", "myuser")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD", "mypassword")

    app = flask.Flask(__name__)
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database.db.init_app(app)
    app.register_blueprint(routes.bp)

    with app.app_context():
        database.db.create_all()

    return app


app = create_app()


@app.route("/", methods=["GET"])
def list_repositories():
    """List Repositories Page."""
    config = configparser.ConfigParser()
    config.read("repositories.cfg")
    repositories = []
    for section in config.sections():
        repository = {"name": section}
        repository.update(config[section])
        repositories.append(repository)
    return flask.render_template("repositories.html", repositories=repositories)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
