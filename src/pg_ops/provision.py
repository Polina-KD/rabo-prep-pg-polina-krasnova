"""Deliver a database to a squad, and remove it again (decommission). Idempotent.

Run:  python -m pg_ops.provision nova            → database nova_db, roles nova_app and nova_reader
      python -m pg_ops.provision nova --remove   → remove them again
Running the same command twice changes nothing the second time.
"""

import re
import sys

from psycopg import sql  # noqa: F401  (you need this in Part E3)

from pg_ops.db import connect  # noqa: F401  (you need this in Part E3)

NAME = re.compile(r"^[a-z][a-z0-9_]{1,30}$")


def role_exists(conn, role: str) -> bool:
    return conn.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (role,)).fetchone() is not None


def database_exists(conn, db: str) -> bool:
    row = conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db,)).fetchone()
    return row is not None


def provision(squad: str) -> list[str]:
    """Create the roles {squad}_app and {squad}_reader and the database {squad}_db.

    Only create what does not exist yet. Return a list of what you changed (empty = no change).
    Tips: use role_exists() and database_exists(). Use sql.Identifier for names.
    CREATE DATABASE cannot run in a transaction: connect(autocommit=True).
    """
    raise NotImplementedError("TODO (Part E3)")


def remove(squad: str) -> list[str]:
    """Remove the database and the two roles (decommissioning). Only remove what exists."""
    raise NotImplementedError("TODO (Part E3)")


if __name__ == "__main__":
    squad = sys.argv[1]
    result = remove(squad) if "--remove" in sys.argv else provision(squad)
    print("\n".join(result) if result else "no change")
