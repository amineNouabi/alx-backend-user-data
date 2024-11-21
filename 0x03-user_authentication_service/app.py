#!/usr/bin/env python3
""" Flask app
"""

from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """ GET /
    Return:
      - welcome message
    """
    return jsonify({"message": "Bienvenue"})
