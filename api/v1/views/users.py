#!/usr/bin/python3
"""endpoint for Users"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users_with_no_id():
    """GET and POST users without id"""
    if request.method == 'GET':
        all_users = storage.all('User')
        all_users = list(obj.to_dict() for obj in all_users.values())
        return jsonify(all_users)

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None:
            abort(400, 'Not a JSON')
        if post_data.get('email') is None:
            abort(400, 'Missing email')
        if post_data.get('password') is None:
            abort(400, 'Missing password')
        user = User(**post_data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_with_id(user_id=None):
    """endpoint for all operations with user_id"""
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(user_obj.to_dict())

    if request.method == 'DELETE':
        user_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')

        ignore = ("id", "email", "created_at", "updated_at")

        # filters data by ignoring the unnecessary
        filtered_data = {k: v for k, v in obj_data.items() if k not in ignore}

        for k, v in filtered_data.items():
            setattr(user_obj, k, v)

        user_obj.save()
        return jsonify(user_obj.to_dict()), 200
