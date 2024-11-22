#!/usr/bin/env python3
""" Flask app
"""

from flask import Flask, jsonify, request, abort, redirect
from flask.helpers import make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """ GET /
    Return:
      - welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ POST /users
    Register a user
    Return:
      - email
      - message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashed=False)
def login():
    """ POST /sessions
    Create a session for user.
    Return:
      - session_id
    """
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(
        jsonify({'email': email, 'message': 'logged in'})
    )
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /sessions, - session_id
    Find user with requested session ID, if exists, destroy session
    Redirect user to GET /, if doesnt exists, respond with 403 HTTP
    status
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return 403 if session ID is invalid
    Use session_id to find user
    """
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
