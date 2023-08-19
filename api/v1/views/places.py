#!/usr/bin/python3
"""
Endpoints for Places
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places_from_cities(city_id=None):
    """GET and POST to places under a city"""
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = [obj.to_dict() for obj in city_obj.places]
        return jsonify(all_places)

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None:
            abort(400, 'Not a JSON')
        if post_data.get("user_id") is None:
            abort(400, 'Missing user_id')
        if post_data.get("name") is None:
            abort(400, 'Missing name')
        users = storage.get('User', post_data['user_id'])
        if users is None:
            abort(404, 'Not found')
        post_data['city_id'] = city_obj.id
        post_data['user_id'] = users.id
        place = Place(**post_data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places_with_placeId(place_id=None):
    """Endpoint for places with place_id"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        ignore = ("id", "user_id", "city_id", "created_at", "updated_at")
        filtered_data = {k: v for k, v in obj_data.items() if k not in ignore}

        for k, v in filtered_data:
            setattr(place_obj, k, v)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
