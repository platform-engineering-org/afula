import configparser

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import request

app = Flask(__name__)
app.config["WTF_CSRF_ENABLED"] = False


@app.route("/")
def list_repositories():
    """List Repositories Page"""
    config = configparser.ConfigParser()
    config.read("repositories.cfg")
    repositories = []
    for section in config.sections():
        repository = {"name": section}
        repository.update(config[section])
        repositories.append(repository)
    return render_template("repositories.html", repositories=repositories)


@app.route("/request-repo", methods=["GET", "POST"])
def request_repo():
    """Request to onboard a Repo Form"""
    form = request.RequestForm()
    if form.validate_on_submit():
        repo_name = form.repo_name.data
        repo_url = form.repo_url.data

        print(f"Requested Repository - Name: {repo_name}, Url: {repo_url}")

        return redirect(url_for("success"))

    return render_template("request_repo.html", form=form)


@app.route("/success")
def success():
    return "Repository request submitted successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
