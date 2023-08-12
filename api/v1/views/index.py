#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def status():
    """returns status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)
