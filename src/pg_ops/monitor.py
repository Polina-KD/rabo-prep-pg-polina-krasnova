"""A small monitoring script: a few checks, each with the status OK or WARNING.

Run:  python -m pg_ops.monitor
"""

from pg_ops.db import connect


def check_connections(used: int, maximum: int, warn_share: float = 0.8) -> str:
    """WARNING when more than 80 % of the allowed connections are in use."""
    return "WARNING" if used > warn_share * maximum else "OK"


def check_replication_lag(lag_bytes: int | None, warn_bytes: int = 16 * 1024 * 1024) -> str:
    """WARNING when there is no replica (None) or the replica is more than 16 MB behind."""
    raise NotImplementedError("TODO (Part D): write this check. The test shows what it must do.")


def check_database_size(size_bytes: int, warn_bytes: int = 1024**3) -> str:
    """WARNING when the database is bigger than 1 GB."""
    raise NotImplementedError("TODO (Part D): write this check.")


def run() -> dict[str, tuple[str, str]]:
    with connect() as conn:
        used = conn.execute("SELECT count(*) FROM pg_stat_activity").fetchone()[0]
        maximum = int(conn.execute("SHOW max_connections").fetchone()[0])
        lag = conn.execute(
            "SELECT max(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn)) FROM pg_stat_replication"
        ).fetchone()[0]
        size = conn.execute("SELECT pg_database_size(current_database())").fetchone()[0]
    return {
        "connections": (check_connections(used, maximum), f"{used} of {maximum}"),
        "replication_lag": (
            check_replication_lag(None if lag is None else int(lag)),
            "no replica" if lag is None else f"{int(lag)} bytes",
        ),
        "database_size": (check_database_size(size), f"{size // 1024} kB"),
    }


if __name__ == "__main__":
    for name, (status, detail) in run().items():
        print(f"{status:8} {name:16} {detail}")
