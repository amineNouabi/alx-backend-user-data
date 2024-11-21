#!/usr/bin/env python3
""" Auth module
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> str:
    """ Returns a hashed password
    """
    import bcrypt
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
