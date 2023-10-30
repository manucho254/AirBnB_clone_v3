#!/usr/bin/python3
""" module to handle all Place object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.city import City
from models.place import Place
from models.user import User


@api_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def city_places(city_id):
    """ Retrives all City cities
    """
    city = storage.get(City, city_id)
    places = []

    if city is None:
        return abort(404)

    tmp = city.places
    for place in tmp:
        places.append(place.to_dict())

    return jsonify(places)


@api_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def place(place_id):
    """ Retrieve Place by id
    """
    place = storage.get(Place, place_id)

    if place is None:
        return abort(404)

    return jsonify(place.to_dict())


@api_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """ Deletes Place object
    """
    place = storage.get(Place, place_id)

    if place is None:
        return abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@api_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """ create new Place
    """
    if storage.get(City, city_id):
        return abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400

    if storage.get(User, data.get("user_id")) is None:
        return abort(404)

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    place = Place(**data)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@api_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object
    """
    place = storage.get(City, city_id)
    data = request.get_json()

    if place is None:
        return abort(404)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(place, key, val)
            place.save()

    return jsonify(place.to_dict()), 200
