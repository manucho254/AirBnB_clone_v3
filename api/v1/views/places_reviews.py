#!/usr/bin/python3
""" module to handle all Review object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@api_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def place_reviews(place_id):
    """ Retrives all Place reviews
    """
    place = storage.get(Place, place_id)
    reviews = []

    if place is None:
        return abort(404)

    tmp = place.reviews
    for review in tmp:
        reviews.append(review.to_dict())

    return jsonify(reviews)


@api_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def review(review_id):
    """ Retrieve Review by id
    """
    review = storage.get(Review, review_id)

    if review is None:
        return abort(404)

    return jsonify(review.to_dict())


@api_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """ Deletes Review object
    """
    review = storage.get(Review, review_id)

    if review is None:
        return abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@api_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """ create new Place
    """
    if storage.get(Place, place_id) is None:
        return abort(404)

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400

    if storage.get(User, data.get("user_id")) is None:
        return abort(404)

    if data.get("text") is None:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**data)
    review.place_id = place_id
    review.save()

    return jsonify(review.to_dict()), 201


@api_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Updates a Place object
    """
    review = storage.get(Review, review_id)
    data = request.get_json()

    if review is None:
        return abort(404)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(review, key, val)
            review.save()

    return jsonify(review.to_dict()), 200
