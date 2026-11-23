"""Connection settings. The address comes from the environment variable DATABASE_URL."""

import os

import psycopg

DEFAULT_URL = "postgresql://postgres:postgres@localhost:55432/delivery"


def database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_URL)


def connect(url: str | None = None, autocommit: bool = False) -> psycopg.Connection:
    return psycopg.connect(url or database_url(), autocommit=autocommit)
