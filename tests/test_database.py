"""Tests against a real database (local: docker compose; CI: the postgres service)."""

import psycopg
import pytest
from conftest import needs_db

from pg_ops.db import connect
from pg_ops.migrate import migrate
from pg_ops.provision import provision, remove

pytestmark = needs_db


def test_migrations_twice_change_nothing():
    migrate()
    assert migrate() == []


def test_tables_exist():
    migrate()
    with connect() as conn:
        rows = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        names = {r[0] for r in rows}
    assert {"bronze_events", "squads", "deployments"} <= names


def test_reader_cannot_write():
    migrate()
    with connect() as conn:
        conn.execute("SET ROLE dashboard_reader")
        conn.execute("SELECT count(*) FROM deployments")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("INSERT INTO squads VALUES ('Test', 'a', 't')")


def test_provision_is_idempotent():
    remove("cisquad")
    assert provision("cisquad") != []
    assert provision("cisquad") == []
    assert remove("cisquad") != []
    assert remove("cisquad") == []
