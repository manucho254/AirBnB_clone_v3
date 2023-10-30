#!/usr/bin/python3
""" view for Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views

from flask import jsonify

from models import storage
from models.amenity import Amenity


@api_views.route("/amenities", methods=["GET"])
def amenities():
    """ Retrives all amenities
    """
    amenities = storage.all(Amenity)

    return jsonify(amenities)


@api_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenity(amenity_id):
    """ Retrieve amenity by id
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(amenity)


@api_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """ Deletes amenity object
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(amenity)
    storage.save()

    return jsonify({})


@api_views.route("/amenities", methods=["POST"])
def create_amenity():
    """ create new amenity
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity), 200


@api_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """ Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()

    if amenity is None:
        return jsonify({"error": "Not found"}), 404

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)
            amenity.save()

    return jsonify(amenity), 200
