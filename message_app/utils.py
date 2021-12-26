import os
from hashlib import sha256
from collections import namedtuple
from typing import NamedTuple

# Hashing return type
HASHING_PACKAGE = namedtuple("Hashing_Package", ["password_hash", "password_salt"])

# Hash function using sha256
# Function returns the password_hash and password_salt
def hashing(password: str, salt = None) -> NamedTuple:
    if not salt:
        salt = os.urandom(5)

    password += str(salt)
    h = sha256()
    h.update(bytes(password, "utf8"))
    password = h.hexdigest()

    return HASHING_PACKAGE(password, salt)