import sqlite3
from dataclasses import dataclass


@dataclass
class URL:
    target_url: str
    key: str
    secret_key: str
    id: int | None = None
    is_active: bool = True
    clicks: int = 0

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "URL":
        return cls(
            id=row["id"],
            key=row["key"],
            secret_key=row["secret_key"],
            target_url=row["target_url"],
            is_active=bool(row["is_active"]),
            clicks=row["clicks"],
        )
