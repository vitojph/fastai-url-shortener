# URL shortener

A small FastAPI app that creates short URLs, forwards visitors, and counts clicks. A delete request sets `is_active` to false. The row stays in SQLite.

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

Settings come from `.env`: `ENV_NAME`, `BASE_URL`, and `DB_URL`.

## Reference

This project follows [Build a URL Shortener With FastAPI and Python](https://realpython.com/build-a-python-url-shortener-with-fastapi/) on Real Python.
