import os

import psycopg
import pytest

from pg_ops.db import database_url


def database_available() -> bool:
    try:
        psycopg.connect(database_url(), connect_timeout=2).close()
        return True
    except psycopg.OperationalError:
        return False


needs_db = pytest.mark.skipif(
    not database_available() and not os.environ.get("CI"),
    reason="no database: start it with 'docker compose up -d'",
)
