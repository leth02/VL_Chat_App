import bcrypt
from collections import namedtuple
from typing import NamedTuple

# Hash function using brcypt
# Function returns the password_hash and password_salt
def hash_pw(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(bytes(password, 'utf8'), salt)

    return password_hash

def check_pw(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(bytes(password, 'utf8'), hashed_password)
