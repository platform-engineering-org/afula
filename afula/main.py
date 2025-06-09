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

from flask import Flask, render_template, redirect, url_for
import register

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


@app.route("/")
def list_repositories():
    """List Repositories Page."""
    config = configparser.ConfigParser()
    config.read("repositories.cfg")
    repositories = []
    for section in config.sections():
        repository = {"name": section}
        repository.update(config[section])
        repositories.append(repository)
    return render_template("repositories.html", repositories=repositories)


@app.route("/register-repo", methods=["GET", "POST"])
def register_repo():
    """Request to onboard a Repo Form."""
    form = register.RequestForm()
    if form.validate_on_submit():
        repo_name = form.repo_name.data
        repo_url = form.repo_url.data

        print(f"Requested Repository - Name: {repo_name}, Url: {repo_url}")

        return redirect(url_for("success"))

    return render_template("request_repo.html", form=form)


@app.route("/success")
def success():
    """Success Message."""
    form = register.RequestForm()
    return "Repository request submitted successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
