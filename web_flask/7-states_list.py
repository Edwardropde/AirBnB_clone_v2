#!/usr/bin/python3
"""
Begins a Flash web application
Application listens on 0.0.0.0., port 5000
Routes:
    /states_list: HTML page with list of all state objects in DBStorage
"""
from models import storage
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    Displays HTML page with list of State objects in DBStorgae
    States sorted by name
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove current SQAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
