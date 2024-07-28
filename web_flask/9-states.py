#!/usr/bin/python3
"""
Script starts a Flask web application:
Requirements:
 - list all states from storage
 - list all cities in a specified state
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def delete_session(exception=None):
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def list_states_cities(id=None):
    # Get list of states
    states = storage.all(State)
    if id is not None:
        state_id = "State." + id
    return render_template('9-states.html', state_id=state_id, states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
