import secrets
import sqlite3
import string

import crud


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: sqlite3.Connection) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
