#!/usr/bin/python3
"""Importing Flask to run the web app
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def states():
    """ Display a list of States in a HTML page """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    cities = storage.all(City)
    places = storage.all(Place)
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places,
                           cities=cities)


@app.teardown_appcontext
def teardown(exc):
    """ Removes current SQLAlchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
