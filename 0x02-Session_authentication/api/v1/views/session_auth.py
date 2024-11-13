#!/usr/bin/env python3
""" Module of Sessiom auth views
"""
from flask import jsonify, make_response, request
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
        return jsonify({ 'error': 'email missing'}), 400
    if not password:
        return jsonify({ 'error': 'password missing'}), 400

    user: User = User.search({ email: email })
    if not user:
        return jsonify({ 'error': 'no user found for this email'}), 404
    if not user.is_valid_password(password):
        return jsonify({ 'error': 'wrong password'}), 401

    from api.v1.app import auth
    
    response = make_response(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), auth.create_session(user.id))
    return response
