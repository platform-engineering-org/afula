"""
Provide the Flask blueprint for repository routes.

Author: Liora Milbaum
"""

import flask

import database
import forms
import models

bp = flask.Blueprint("repos", __name__, url_prefix="/repos")


@bp.route("/list", methods=["GET"])
def list_repos():
    """List Repositories."""
    repos = models.Repo.query.all()
    return flask.render_template("repos.html", repos=repos)


@bp.route("/register", methods=["GET", "POST"])
def register_repo():
    """Request to onboard a Repo Form."""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        new_repo = models.Repo(name=form.repo_name.data, url=form.repo_url.data)
        database.db.session.add(new_repo)
        database.db.session.commit()
        return flask.redirect(flask.url_for("repos.success"))

    return flask.render_template("register_form.html", form=form)


@bp.route("/success", methods=["GET"])
def success():
    """Success Message."""
    return "Repository has been registered successfully.!"
