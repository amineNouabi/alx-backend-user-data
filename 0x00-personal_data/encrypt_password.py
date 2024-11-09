#!/usr/bin/env python3

"""
Module for hashing password function
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hash password function"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password is valid"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
