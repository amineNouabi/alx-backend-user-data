#!/usr/bin/env python3

""" Basic Auth Module
"""

from api.v1.auth.auth import Auth
from base64 import b64decode

class BasicAuth(Auth):
    """ Basic Auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract authorization header
        """
        if authorization_header is None \
                or not isinstance(authorization_header, str) \
                or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decodes base64 authorization token
        """
        if base64_authorization_header is None \
            or not isinstance(base64_authorization_header, str):
                return None
        try:
             return b64decode(base64_authorization_header.encode("utf-8")).decode("utf-8")
        except:
             return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> tuple[str]:
        """ Extract user credentials
        """
        if decoded_base64_authorization_header is None \
            or not isinstance(decoded_base64_authorization_header, str) \
            or len(decoded_base64_authorization_header.split(":")) != 2:
             return (None, None)
        email, password = decoded_base64_authorization_header.split(":")
        return email, password
