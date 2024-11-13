#!/usr/bin/env python3
""" Module of Sessiom auth views
"""
from typing import List
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from os import getenv
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """ Session auth login endpoint
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    try:
        user: List[User] = User.search({'email': email})
        if not user or not len(user):
            return jsonify({'error': 'no user found for this email'}), 404
        if not user[0].is_valid_password(password):
            return jsonify({'error': 'wrong password'}), 401

        from api.v1.app import auth
        response = make_response(user[0].to_json())
        response.set_cookie(getenv("SESSION_NAME"),
                            auth.create_session(user[0].id))
        return response
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ Session auth logout endpoint
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
