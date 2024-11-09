#!/usr/bin/env python3

"""Module for filter_datum function"""

import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = re.sub(
            f"({"|".join(self.fields)})=(.*?)(?={self.SEPARATOR}|$)", r"\1=" + self.REDACTION, record.msg)
        return super(RedactingFormatter, self).format(record)

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """Replaces indecated sensitive fields values to redaction."""
    return re.sub(f"({"|".join(fields)})=(.*?)(?={separator}|$)", r"\1=" + redaction, message)
