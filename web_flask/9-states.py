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
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def state():
    """
    Displays HTML page with list of states
    States sorted by name
    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def state_by_id(id):
    """
    Displays HTML page with infor on <id> if it exists
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def close(self):
    """Remove current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
