#!/usr/bin/python3
""" module to handle all City object RESTFul Api actions
"""
from api.v1.views import app_views

from flask import jsonify

from models import storage
from models.state import State
from modesl.city import City


@api_views.route("/states/<state_id>/cities", methods=["GET"])
def state_cities(state_id):
    """ Retrives all State cities
    """
    state = storage.get(State, state_id)

    if state is None:
        return jsonify({"error": "Not found"}), 404

    cities = state.cities()
    return jsonify(cities)


@api_views.route("/cities/<city_id>", methods=["GET"])
def city(city_id):
    """ Retrieve City by id
    """
    city = storage.get(City, city_id)

    if city is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(city)


@api_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ Deletes City object
    """
    city = storage.get(City, city_id)

    if city is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(city)
    storage.save()

    return jsonify({})


@api_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city():
    """ create new City
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    city = City(**data)
    city.save()

    return jsonify(city), 200


@api_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """ Updates a City object
    """
    city = storage.get(City, city_id)
    data = request.get_json()

    if city is None:
        return jsonify({"error": "Not found"}), 404

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(city, key, val)
            city.save()

    return jsonify(city), 200
