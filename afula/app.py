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

import forms
import models


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
    models.db.init_app(app)

    with app.app_context():
        models.db.create_all()

    return app


app = create_app()


@app.route("/list", methods=["GET"])
def list_repos():
    """List Repositories."""
    repos = models.Repo.query.all()
    return flask.render_template("repos.html", repos=repos)


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


@app.route("/register-repo", methods=["GET", "POST"])
def register_repo():
    """Request to onboard a Repo Form."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        repo_name = form.repo_name.data
        repo_url = form.repo_url.data

        print(f"Repository Registered - Name: {repo_name}, Url: {repo_url}")

        return flask.redirect(flask.url_for("success"))

    return flask.render_template("register_form.html", form=form)


@app.route("/success", methods=["GET"])
def success():
    """Success Message."""
    return "Repository has been registered successfully.!"


def init():
    """Initialize the db."""
    with app.app_context():
        models.db.create_all()


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=5000, debug=True)
