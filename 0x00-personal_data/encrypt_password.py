#!/usr/bin/env python3

"""
Module for hashing password function
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash password function"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")
