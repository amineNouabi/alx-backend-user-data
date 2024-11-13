#!/usr/bin/env python3

""" Session Expiration Auth Module
"""
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
        session = UserSession({'id': session_id, 'user_id': user_id})
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user_id from session_id
        """
        if not session_id:
            return None
        session: UserSession = UserSession.get(session_id)
        if not session:
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """ Destroys session
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        session: UserSession = UserSession.get(session_id)
        if not session:
            return False
        super().destroy_session(request)
        session.remove()
        return True
