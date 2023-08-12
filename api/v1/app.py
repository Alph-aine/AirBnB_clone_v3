#!/usr/bin/python3
"""Flask app for the AirBnB clone"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# flask environment setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')

# registering app with app_views blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes current sqlAlchemy session after each request"""
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
