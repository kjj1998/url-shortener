#!/bin/sh

# poetry run alembic upgrade heads

# poetry run uvicorn url_shortener.web.app:app --host 0.0.0.0 --port 8000 --reload

alembic upgrade heads
uvicorn url_shortener.web.app:app --host 0.0.0.0 --port 8000 --reload