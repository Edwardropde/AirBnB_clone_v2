#!/usr/bin/python3
"""
Begins Flask web application
Application listens on 0.0.0.0., port 5000
Routes:
    /states: HTML page with list of state objects
    /states/<id>: HTML page displaying state with <id>
"""
from models import storage
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """
    Displays HTML page with list of states
    States sorted by name
    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    Displays HTML page with infor on <id> if it exists
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(self):
    """Remove current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
