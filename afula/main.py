import configparser

from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
