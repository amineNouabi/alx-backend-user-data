#!/usr/bin/env python3

""" Session Auth Module
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar

from models.user import User

UserType = TypeVar('User')


class SessionAuth(Auth):
    """ Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str) -> str:
        """ Create a session for a user.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get User id by session Id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> UserType:
        """ Gets current user from cookies
        """
        return User.get(
            self.user_id_for_session_id(
                self.session_cookie(request)
            )
        )

    def destroy_session(self, request=None):
        """ Log out and destroy session
        """
        session_id = self.session_cookie(request)
        if request is None or not session_id \
                or not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
