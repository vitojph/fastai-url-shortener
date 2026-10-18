import sqlite3

import keygen
import models
import schemas


def create_db_url(db: sqlite3.Connection, url: schemas.URLBase) -> models.URL:
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}-{keygen.create_random_key(8)}"
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    cursor = db.execute(
        """
        INSERT INTO urls ("key", secret_key, target_url, is_active, clicks)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            db_url.key,
            db_url.secret_key,
            db_url.target_url,
            int(db_url.is_active),
            db_url.clicks,
        ),
    )
    db.commit()
    db_url.id = cursor.lastrowid
    return db_url


def get_db_url_by_key(db: sqlite3.Connection, url_key: str) -> models.URL | None:
    row = db.execute(
        """
        SELECT id, "key", secret_key, target_url, is_active, clicks
        FROM urls
        WHERE "key" = ? AND is_active = 1
        """,
        (url_key,),
    ).fetchone()
    if row is None:
        return None
    return models.URL.from_row(row)


def get_db_url_by_secret_key(
    db: sqlite3.Connection, secret_key: str
) -> models.URL | None:
    row = db.execute(
        """
        SELECT id, "key", secret_key, target_url, is_active, clicks
        FROM urls
        WHERE secret_key = ? AND is_active = 1
        """,
        (secret_key,),
    ).fetchone()
    if row is None:
        return None
    return models.URL.from_row(row)


def update_db_clicks(db: sqlite3.Connection, db_url: models.URL) -> models.URL:
    db_url.clicks += 1
    db.execute(
        "UPDATE urls SET clicks = ? WHERE id = ?",
        (db_url.clicks, db_url.id),
    )
    db.commit()
    return db_url


def deactivate_db_url_by_secret_key(
    db: sqlite3.Connection, secret_key: str
) -> models.URL | None:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.execute(
            "UPDATE urls SET is_active = ? WHERE id = ?",
            (int(db_url.is_active), db_url.id),
        )
        db.commit()
    return db_url
