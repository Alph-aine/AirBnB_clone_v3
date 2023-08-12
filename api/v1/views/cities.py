#!/usr/bin/python3
"""returns all the details about cities in a state"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_state_with_id(state_id=None):
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        state_obj.name = obj_data['name']
        state_obj.save()
        return jsonify(state_obj.to_dict()), 200
