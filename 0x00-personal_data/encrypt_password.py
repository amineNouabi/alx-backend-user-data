#!/usr/bin/env python3

"""
Module for hashing password function
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash password function"""
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
