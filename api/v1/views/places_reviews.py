#!/usr/bin/python3
"""
Endpoints for places reviews
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews_from_places(place_id=None):
    """endpoints for places reviews"""
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_reviews = storage.all('Review')
        place_review = [obj.to_dict() for obj in all_reviews.values()
                        if obj.place_id == place_id]
        return jsonify(place_review)

    if request.method == 'POST':
        post_data = request.get_json()
        if post_data is None:
            abort(400, 'Not a JSON')
        if post_data.get('user_id') is None:
            abort(400, 'Missing user_id')
        user = storage.get('User', post_data['user_id'])
        if user is None:
            abort(404, 'Not found')
        if post_data.get('Text') is None:
            abort(400, 'Missing Text')

        post_data['user_id'] = user.id
        post_data['place_id'] = place_obj.id
        review = Review(**post_data)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviews_with_reviewId(review_id=None):
    """Endpoints for reviews using review id"""
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj.delete()
        return jsonify({}), 200

    if request.method == 'PUT':
        obj_data = request.get_json()
        if obj_data is None:
            abort(400, 'Not a JSON')

        ignore = ("id", "user_id", "place_id", "created_at", "updated_at")
        filtered_data = {k: v for k, v in obj_data.items() if k not in ignore}
        for k, v in filtered_data:
            setattr(review_obj, k, v)

        review_obj.save()
        return jsonify(review_obj.to_dict()), 200
