import sqlite3

from config import get_settings


def sqlite_path(db_url: str) -> str:
    prefix = "sqlite:///"
    if not db_url.startswith(prefix):
        raise ValueError(f"DB_URL must start with {prefix}")
    return db_url[len(prefix) :]


def connect() -> sqlite3.Connection:
    # FastAPI may open this connection in one thread and use it in another.
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    db = connect()
    try:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER NOT NULL,
                "key" VARCHAR,
                secret_key VARCHAR,
                target_url VARCHAR,
                is_active BOOLEAN,
                clicks INTEGER,
                PRIMARY KEY (id),
                UNIQUE (target_url)
            )
            """
        )
        db.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_urls_key ON urls ("key")')
        db.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_urls_secret_key ON urls (secret_key)"
        )
        db.commit()
    finally:
        db.close()


DB_PATH = sqlite_path(get_settings().db_url)
