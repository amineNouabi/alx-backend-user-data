#!/usr/bin/env python3

"""Module for filter_datum function"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """Replaces indecated sensitive fields values to redaction."""
    return re.sub(f"({"|".join(fields)})=(.*?)(?={separator}|$)", r"\1=" + redaction, message)
