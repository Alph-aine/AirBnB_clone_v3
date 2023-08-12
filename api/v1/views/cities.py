#!/usr/bin/python3
"""returns all the details about cities in a state"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities_with_stateId(state_id=None):
    """returns all cities in a state"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all("City")
        cities_in_state = [obj.to_dict() for obj in all_cities.values()
                           if obj.state_id == state_id]
        return jsonify(cities_in_state)

    if request.method == 'POST':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        if obj_data.get('name') is None:
            abort(400, 'Missing name')
        obj_data['state_id'] = state_id
        obj = City(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id=None):
    """returns city havng the city id"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_dict())

    if request.method == 'DELETE':
        city_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        city_obj.name = obj_data['name']
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
