"""Validadores compartidos."""

import re

PHONE_PATTERN = re.compile(r"^(\+|0)[0-9]{6,20}$")


def validate_phone(value: str) -> bool:
    return bool(PHONE_PATTERN.match(value))



