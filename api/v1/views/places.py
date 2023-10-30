#!/usr/bin/python3
""" module to handle all Place object RESTFul Api actions
"""
from api.v1.views import app_views

from flask import jsonify

from models import storage
from models.city import City
from modesl.place import Place


@api_views.route("/states/<state_id>/cities", methods=["GET"])
def city_places(city_id):
    """ Retrives all City cities
    """
    city = storage.get(City, city_id)

    if city is None:
        return jsonify({"error": "Not found"}), 404

    places = city.places()
    return jsonify(places)


@api_views.route("/places/<place_id>", methods=["GET"])
def place(place_id):
    """ Retrieve Place by id
    """
    place = storage.get(Place, place_id)

    if place is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(place)


@api_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """ Deletes Place object
    """
    place = storage.get(Place, place_id)

    if place is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(place)
    storage.save()

    return jsonify({})


@api_views.route("/cities/<city_id>/cities", methods=["POST"])
def create_place():
    """ create new Place
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    place = Place(**data)
    place.save()

    return jsonify(place), 200


@api_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """ Updates a Place object
    """
    place = storage.get(City, city_id)
    data = request.get_json()

    if city is None:
        return jsonify({"error": "Not found"}), 404

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(place, key, val)
            place.save()

    return jsonify(place), 200
