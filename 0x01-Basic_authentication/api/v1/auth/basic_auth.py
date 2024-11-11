#!/usr/bin/env python3

""" Basic Auth Module
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ E
        """
        if authorization_header is None \
                or not isinstance(authorization_header, str) \
                or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]
