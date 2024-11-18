#!/usr/bin/env python3

""" Module defining User model
"""

from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """ User Model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __init__(self, email, hashed_password, *args, **kwargs):
        """ Constructor
        """
        if email and hashed_password:
            self.email = email
            self.hashed_password = hashed_password
        elif kwargs:
            self.email = kwargs.get('email', '')
            self.hashed_password = kwargs.get('hashed_password', '')
        elif len(args) == 2:
            self.email = args[0]
            self.hashed_password = args[1]
