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
    if not NAME.fullmatch(squad):
        raise ValueError("Invalid squad name")

    db = f"{squad}_db"
    app_role = f"{squad}_app"
    reader_role = f"{squad}_reader"

    changes = []

    with connect(autocommit=True) as conn:
        # Create the database first
        if not database_exists(conn, db):
            conn.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(db)
                )
            )
            changes.append(f"Created database {db}")

        # Create application role
        if not role_exists(conn, app_role):
            conn.execute(
                sql.SQL("CREATE ROLE {}").format(
                    sql.Identifier(app_role)
                )
            )
            changes.append(f"Created role {app_role}")

        # Create reader role
        if not role_exists(conn, reader_role):
            conn.execute(
                sql.SQL("CREATE ROLE {}").format(
                    sql.Identifier(reader_role)
                )
            )
            changes.append(f"Created role {reader_role}")

    return changes


def remove(squad: str) -> list[str]:
    """Remove the database and the two roles (decommissioning). Only remove what exists."""
    if not NAME.fullmatch(squad):
        raise ValueError("Invalid squad name")

    db = f"{squad}_db"
    app_role = f"{squad}_app"
    reader_role = f"{squad}_reader"

    changes = []

    with connect(autocommit=True) as conn:
        # Remove the database first
        if database_exists(conn, db):
            conn.execute(
                sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(db)
                )
            )
            changes.append(f"Removed database {db}")

        # Remove application role
        if role_exists(conn, app_role):
            conn.execute(
                sql.SQL("DROP ROLE {}").format(
                    sql.Identifier(app_role)
                )
            )
            changes.append(f"Removed role {app_role}")

        # Remove reader role
        if role_exists(conn, reader_role):
            conn.execute(
                sql.SQL("DROP ROLE {}").format(
                    sql.Identifier(reader_role)
                )
            )
            changes.append(f"Removed role {reader_role}")

    return changes


if __name__ == "__main__":
    squad = sys.argv[1]
    result = remove(squad) if "--remove" in sys.argv else provision(squad)
    print("\n".join(result) if result else "no change")
