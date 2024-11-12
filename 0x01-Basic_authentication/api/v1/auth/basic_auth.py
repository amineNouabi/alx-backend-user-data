#!/usr/bin/env python3

""" Basic Auth Module
"""

from flask import request
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import List, TypeVar
from models.user import User


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decodes base64 authorization token
        """
        if base64_authorization_header is None \
                or not isinstance(base64_authorization_header, str):
            return None
        try:
            return b64decode(
                base64_authorization_header.encode("utf-8")
            ).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials
        """
        if decoded_base64_authorization_header is None \
                or not isinstance(decoded_base64_authorization_header, str) \
                or ":" not in decoded_base64_authorization_header:
            return (None, None)
        email_password = decoded_base64_authorization_header.split(":", 1)
        return email_password[0], email_password[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Search for user object from credentials.
        """
        if user_pwd is None or not isinstance(user_pwd, str) \
                or user_email is None or not isinstance(user_email, str):
            return None
        users: List[User] = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns user object that is requesting
        """
        email, password = self.extract_user_credentials(
            self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(
                    self.authorization_header(request)
                )
            )
        )
        return self.user_object_from_credentials(email, password)
