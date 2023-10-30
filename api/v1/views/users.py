#!/usr/bin/python3
""" module to handle all User object RESTFul Api actions
"""
from api.v1.views import app_views as api_views

from flask import jsonify, request, abort

from models import storage
from models.user import User


@api_views.route("/users", methods=["GET"])
def users():
    """ Retrives all users
    """
    users = storage.all(User)

    return jsonify(users)


@api_views.route("/users/<user_id>", methods=["GET"])
def user(user_id):
    """ Retrieve User by id
    """
    user = storage.get(User, user_id)

    if user is None:
        return abort(404)

    return jsonify(user.to_dict())


@api_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Deletes User object
    """
    user = storage.get(User, user_id)

    if user is None:
        return abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})


@api_views.route("/users", methods=["POST"])
def create_user():
    """ create new User
    """
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("email") is None:
        return jsonify({"error": "Missing email"}), 400

    if data.get("password") is None:
        return jsonify({"error": "Missing password"}), 400

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@api_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """ Updates a User object
    """
    user = storage.get(User, user_id)
    data = request.get_json()

    if user is None:
        return abort(404)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "email", "created_at", "updated_at"]

    for key, val in data.items():
        if key not in ignore_keys:
            setattr(user, key, val)
            user.save()

    return jsonify(user.to_dict()), 200
