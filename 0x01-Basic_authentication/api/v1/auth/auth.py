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
        if path is None or exclude_paths is None or not len(exclude_paths):
            return True
        if path[-1] != '/':
            path = f'{path}/'
        for exclude_path in exclude_paths:
            if exclude_path[-1] == "*" and path.startswith(exclude_path[:-1]) \
                    or path == exclude_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets current logged in user
        """
        return None
