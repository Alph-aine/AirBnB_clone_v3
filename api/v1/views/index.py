#!/usr/bin/python3
"""route to api status response"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """returns status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def stats():
    """returns the numbers of each objects by type"""
    if request.method == 'GET':
        response = {}
        OBJECTS = {
             "Amenity": "amenities",
             "City": "cities",
             "Place": "places",
             "Review": "reviews",
             "State": "states",
             "User": "users"
          }
        for key, value in OBJECTS.items():
            response[value] = storage.count(key)
        return jsonify(response)
