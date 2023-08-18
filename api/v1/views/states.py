#!/usr/bin/python3
"""
returns all the details about State
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_all_states():
    """returns all states in storage when no id is provided"""
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = list(obj.to_dict() for obj in all_states.values())
        return jsonify(all_states)

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None:
            abort(400, 'Not a JSON')
        if post_data.get("name") is None:
            abort(400, 'Missing name')
        obj = State(**post_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_with_id(state_id=None):
    """performs operation on a specific state object"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        state_obj.name = obj_data['name']
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200
