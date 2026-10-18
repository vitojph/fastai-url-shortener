# URL shortener

A small FastAPI app that creates short URLs, forwards visitors, and counts clicks. A delete request sets `is_active` to false. The row stays in the SQLite file.

The app opens that file with the standard library `sqlite3` module. It does not use SQLAlchemy. On startup it creates the `urls` table if the table is missing.

## Run

```bash
uv run fastapi dev main.py
```

Open http://127.0.0.1:8000/docs to try the API.

| Method | Path | Action |
| --- | --- | --- |
| `GET` | `/` | Welcome message |
| `POST` | `/url` | Create a short URL |
| `GET` | `/{url_key}` | Forward to the target URL |
| `GET` | `/admin/{secret_key}` | Show admin info and click count |
| `DELETE` | `/admin/{secret_key}` | Deactivate the short URL |

Settings come from `.env`: `ENV_NAME`, `BASE_URL`, and `DB_URL`. `DB_URL` must start with `sqlite:///`. The default is `sqlite:///./shortener.db`, which opens `shortener.db` in the current directory.

## Reference

This project follows [Build a URL Shortener With FastAPI and Python](https://realpython.com/build-a-python-url-shortener-with-fastapi/) on Real Python. The article stores rows with SQLAlchemy. This app stores them with `sqlite3` instead.
