#!/usr/bin/env python3

""" Session Expiration Auth Module
"""
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration Auth class
    """

    def __init__(self) -> None:
        """ Session Expire Constructor
        """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create expirable session
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionExpAuth.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.utcnow()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user_id from session_id
        """
        session = SessionExpAuth.user_id_by_session_id.get(session_id)
        if session_id is None or session is None:
            return None
        if self.session_duration <= 0:
            return session.get("user_id")
        if not session.get("created_at"):
            return None
        if session.get("created_at") + \
            timedelta(seconds=self.session_duration) <= \
                datetime.utcnow():
            return None
        return session.get("user_id")
