#!/usr/bin/env python3
""" Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from db import DB
from user import User


def _hash_password(password: str) -> str:
    """ Returns a hashed password
    """
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def _generate_uuid() -> str:
    """ Generates a new uuid.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user
        """
        if not email or not password:
            raise ValueError("email and password must be set")
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ Except email and password returns validity.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode(),
                user.hashed_password.encode()
            )
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """ Creates a new session for email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass
        return None
