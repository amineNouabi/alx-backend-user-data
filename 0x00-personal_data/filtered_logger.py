#!/usr/bin/env python3

"""Module for filtering sensitive Data."""

import re
import logging
import csv

from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        """Formats and Hide sensitive data mentionned in fields"""
        record.msg = re.sub(
            f"({'|'.join(self.fields)})=(.*?)(?={self.SEPARATOR}|$)",
            r"\1=" + self.REDACTION,
            record.msg
        )
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Replaces indecated sensitive fields values to redaction."""
    return re.sub(f"({'|'.join(fields)})=(.*?)(?={separator}|$)",
                  r"\1=" + redaction,
                  message)


def get_logger() -> logging.Logger:
    """Create Custom logger to format PII fields values"""
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger
