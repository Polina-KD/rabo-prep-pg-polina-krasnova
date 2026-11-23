"""Apply SQL migrations in order. Idempotent: a migration that ran before is skipped.

Run:  python -m pg_ops.migrate            (folder: migrations/)
"""

import sys
from pathlib import Path

from pg_ops.db import connect

MIGRATIONS = Path("migrations")


def pending(applied: set[str], folder: Path = MIGRATIONS) -> list[Path]:
    """Return the migration files that did not run yet, in name order (V001, V002, ...)."""
    return [f for f in sorted(folder.glob("V*.sql")) if f.name not in applied]


def migrate(folder: Path = MIGRATIONS) -> list[str]:
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            " name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
        )
        applied = {row[0] for row in conn.execute("SELECT name FROM schema_migrations")}
        done = []
        for file in pending(applied, folder):
            conn.execute(file.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO schema_migrations (name) VALUES (%s)", (file.name,))
            done.append(file.name)
        conn.commit()
    return done


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else MIGRATIONS
    names = migrate(folder)
    print("applied:", ", ".join(names) if names else "nothing (no change)")
