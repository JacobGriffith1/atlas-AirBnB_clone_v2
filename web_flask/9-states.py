#!/usr/bin/python3
"""Script that starts a Flask web app"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Displays 'C' and the value of 'text'"""
    return 'C %s' % text.replace('_', ' ')


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def py_text(text='is cool'):
    """Displays 'Python' and the value of 'text'"""
    return 'Python %s' % text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """Displays 'n is a number' ONLY if n is an integer"""
    return "%d is a number" % n


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays an HTML page ONLY if n is an integer"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def num_odd_even(n):
    """Displays an HTML page ONLY if n is an integer, and it's odd/even"""
    return render_template('6-number_odd_or_even.html', number=n)


@app.route('/states_list', strict_slashes=False)
def display_html():
    """Displays HTML page inside the tag BODY"""
    from models import storage
    from models.state import State
    states = storage.all(State)
    dict_to_html = {value.id: value.name for value in states.values()}
    return render_template('7-states_list.html',
                           Table="States",
                           items=dict_to_html)


@app.route('/cities_by_states', strict_slashes=False)
def display_cities():
    """Displays HTML page featuring cities by state"""
    from models import storage
    from models.state import State
    from models.city import City
    states = storage.all(State)
    cities = storage.all(City)
    return render_template('8-cities_by_states.html',
                           Table="States",
                           states=states,
                           cities=cities)


@app.route('/states/', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def display_states(id=None):
    """Displays HTML page featuring states"""
    from models import storage
    from models.state import State
    states = storage.all(State)

    if not id:
        dict_to_html = {value.id: value.name for value in states.values()}
        return render_template('7-states_list.html',
                               Table="States",
                               items=dict_to_html)

    s = "State.{}".format(id)
    if s in states:
        state = states[s]
        return render_template('9-states.html',
                               Table="State",
                               state=state)

    return render_template('9-states.html',
                           items=None)


@app.teardown_appcontext
def teardown():
    """Teardown"""
    from models import storage
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
