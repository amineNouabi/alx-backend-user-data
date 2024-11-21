#!/usr/bin/env python3
""" Auth module
"""


def _hash_password(password: str) -> str:
    """ Returns a hashed password
    """
    import bcrypt
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
