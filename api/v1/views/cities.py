#!/usr/bin/python3
""" module to handle all City object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.state import State
from models.city import City


@api_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def state_cities(state_id):
    """ Retrives all State cities
    """
    state = storage.get(State, state_id)
    cities = []

    if state is None:
        return abort(404)

    tmp = state.cities
    for city in tmp:
        cities.append(city.to_dict())

    return jsonify(cities)


@api_views.route("/cities/<city_id>",
                 methods=["GET"], strict_slashes=False)
def city(city_id):
    """ Retrieve City by id
    """
    city = storage.get(City, city_id)

    if city is None:
        return abort(404)

    return jsonify(city.to_dict())


@api_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes City object
    """
    city = storage.get(City, city_id)

    if city is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@api_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """ create new City
    """
    if storage.get(State, state_id) is None:
        return abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    city = City(**data)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@api_views.route("/cities/<city_id>",
                 methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object
    """
    city = storage.get(City, city_id)
    data = request.get_json()

    if city is None:
        abort(404)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(city, key, val)
            city.save()

    return jsonify(city.to_dict()), 200
