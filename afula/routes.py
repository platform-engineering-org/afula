"""
Provide the Flask blueprint for repository routes.

Author: Liora Milbaum
"""

import flask

import forms
import models

bp = flask.Blueprint("repos", __name__, url_prefix="/repos")


@bp.route("/list", methods=["GET"])
def list_repos():
    """List Repositories."""
    repos = models.Repo.query.all()
    return flask.render_template("repos.html", repos=repos)


@bp.route("/register-repo", methods=["GET", "POST"])
def register_repo():
    """Request to onboard a Repo Form."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        repo_name = form.repo_name.data
        repo_url = form.repo_url.data

        print(f"Repository Registered - Name: {repo_name}, Url: {repo_url}")

        return flask.redirect(flask.url_for("success"))

    return flask.render_template("register_form.html", form=form)


@bp.route("/success", methods=["GET"])
def success():
    """Success Message."""
    return "Repository has been registered successfully.!"
