"""
Provide the Flask blueprint for repository routes.

Author: Liora Milbaum
"""

import flask

from . import database, forms, models

bp = flask.Blueprint("repos", __name__, url_prefix="/repos")


@bp.route("/list", methods=["GET"])
def list_repos():
    """List Repositories."""
    repos = models.Repo.query.all()
    return flask.render_template("repos.html", repos=repos)


@bp.route("/register", methods=["GET", "POST"])
def register_repo():
    """
    Handle repository registration via HTML form or JSON payload.

    - For JSON: expects a POST request with fields `repo_name` and `repo_url`.
    - For UI: handles form submission via WTForms.
    """
    if flask.request.is_json:
        data = flask.request.get_json()
        repo_name = data.get("name")
        repo_url = data.get("url")

        if not repo_name or not repo_url:
            return flask.jsonify({"error": "Missing required fields"}), 400

        new_repo = models.Repo(name=repo_name, url=repo_url)
        database.db.session.add(new_repo)
        database.db.session.commit()
        return flask.jsonify(
            {"message": f"Repository '{repo_name}' registered successfully"}
        ), 201
    else:
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
