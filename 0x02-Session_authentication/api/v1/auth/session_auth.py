#!/usr/bin/env python3

""" Session Auth Module
"""

from api.v1.auth.auth import Auth
from uuid import uuid4

class SessionAuth(Auth):
    """ Session Auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str) -> str:
        """ Create a session for a user.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
