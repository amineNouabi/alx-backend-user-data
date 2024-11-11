#!/usr/bin/env python3

""" Auth Module
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth System Class
    """

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """ Require auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets current logged in user
        """
        return None
