#!/usr/bin/python3
"""endpoint for amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenity():
    """GETS all amenities from storage"""
    if request.method == 'GET':
        all_amenity = storage.all('Amenity')
        all_amenity = list(obj.to_dict() for obj in all_amenity.values())
        return jsonify(all_amenity)

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None:
            abort(400, 'Not a JSON')
        if post_data.get('name') is None:
            abort(400, 'Missing name')
        obj = Amenity(**post_data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_with_id(amenity_id=None):
    """Endpoint for all operations that can be perform using amenity id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')
        amenity_obj.name = obj_data['name']
        amenity_obj.save()
        return jsonify(amenity_obj.to_dict()), 200
