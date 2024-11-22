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


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password, - email,
    Returns 403 status code if email not registered
    Generate token and respond with 200 HTTP status if exists
    """
    email = request.form.get('email', '')
    if not AUTH.create_session(email):
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password, - email, - reset_token, - new_password
    Return a 403 HTTP code if token is invalid
    if valid, respond with 200 HTTP code
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
