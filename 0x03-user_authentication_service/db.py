#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds user to database and returns user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Finds user by selected column and value.
        """
        user_fields = ['id',
                       'email',
                       'hashed_password',
                       'reset_token',
                       'session_id']
        for key in kwargs.keys():
            if key not in user_fields:
                raise InvalidRequestError
        user = self.__session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user
