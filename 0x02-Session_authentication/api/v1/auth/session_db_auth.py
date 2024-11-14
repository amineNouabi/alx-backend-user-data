#!/usr/bin/env python3

""" Session Expiration Auth Module
"""

from typing import List
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ Session DB Expiration Auth class
    """

    def create_session(self, user_id=None):
        """ Create expirable DB session
        """
        session_id = super().create_session(user_id)
        if user_id is None or session_id is None:
            return None
        session = UserSession()
        session.user_id = user_id
        session.session_id = session_id
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user_id from session_id
        """
        if not session_id:
            return None
        try:
            session: UserSession = UserSession.search(
                {'session_id': session_id}
            )[0]
            if self.session_duration <= 0:
                return session.get("user_id")
            if not session.get("created_at"):
                return None
            if session.get("created_at") + \
                timedelta(seconds=self.session_duration) <= \
                    datetime.now():
                return None
            return session.get("user_id")
        except Exception:
            return None

    def destroy_session(self, request=None):
        """ Destroys session
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            session: UserSession = UserSession.search(
                {'session_id': session_id}
            )
            if not session or not len(session):
                return False
            session[0].remove()
            return True
        except Exception:
            return False
