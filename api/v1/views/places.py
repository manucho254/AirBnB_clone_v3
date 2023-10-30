#!/usr/bin/python3
""" module to handle all Place object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.city import City
from models.place import Place
from models.state import State
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
    if storage.get(City, city_id) is None:
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
    place = storage.get(Place, place_id)
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


@api_views.route("/places_search",
                 methods=["POST"], strict_slashes=False)
def places_search():
    """
    """
    data = request.get_json()
    places = [place.to_dict() for place in storage.all(Place).values()]
    state_ids = data.get("states")
    city_ids = data.get("cities")
    amenity_ids = data.get("amenities")

    print(data)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if len(data) == 0 or sum([len(obj) for obj in data.values()]) == 0:
        return jsonify(filter_by_amenities(places, amenity_ids))

    if len(state_ids) > 0 and city_ids is None:
        places = get_state_places(data, state_ids)
        return jsonify(filter_by_amenities(places, amenity_ids))

    if state_ids is None and len(city_ids) > 0:
        places = get_city_places(data, city_ids)
        return jsonify(filter_by_amenities(places, amenity_ids))

    all_places = get_city_places(data, city_ids)
    for place in get_state_places(data, state_ids):
        if place not in all_places:
            all_places.append(place)

    return jsonify(filter_by_amenities(all_places, amenity_ids))


def get_state_places(data: dict, states: dict):
    """ get all places in a State
    """
    cities = []
    places = []

    for state_id in data.get("states"):
        state = storage.get(State, state_id)
        if state:
            cities.extend(state.cities)

    for city in cities:
        for place in city.places:
            tmp = place.to_dict()
            if tmp.get("amenity_ids"):
                del tmp["amenity_ids"]
            places.append(tmp)

    return places


def get_city_places(data: dict, cities: dict):
    """ Get all places in a city
    """
    places = []

    for city_id in data.get("cities"):
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                tmp = place.to_dict()
                if tmp.get("amenity_ids"):
                    del tmp["amenity_ids"]
                places.append(tmp)

    return places


def filter_by_amenities(places: list, amenities):
    """ filter data by amenities
    """
    filtered = []

    if amenities is None:
        return places

    for place in places:
        if set(place.amenity_ids) == set(amenities):
            tmp = place.to_dict()
            if tmp.get("amenity_ids"):
                del tmp["amenity_ids"]
            filtered.append(tmp)

    return filtered
