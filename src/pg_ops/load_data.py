"""Load the invented deployment data: raw JSON into bronze_events, then clean rows into deployments.

Run:  python -m pg_ops.load_data           (folder: data/)
Idempotent: running it again adds nothing new.
"""

import csv
import json
from pathlib import Path

from psycopg.types.json import Jsonb

from pg_ops.db import connect

DATA = Path("data")

CLEAN_SQL = """
INSERT INTO deployments (event_id, squad, service, environment, status, started_at, duration_s)
SELECT DISTINCT ON (raw->>'event_id')
       raw->>'event_id',
       raw->>'squad',
       raw->>'service',
       raw->>'environment',
       lower(trim(raw->>'status')),
       CASE
         WHEN raw->>'started_at' ~ '^[0-9]+$'
           THEN to_timestamp((raw->>'started_at')::bigint / 1000.0)
         WHEN raw->>'started_at' ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}T'
           THEN (raw->>'started_at')::timestamptz
         WHEN raw->>'started_at' ~ '^[0-9]{2}-[0-9]{2}-[0-9]{4} '
           THEN to_timestamp(raw->>'started_at', 'DD-MM-YYYY HH24:MI')
       END AS started_at,
       (raw->>'duration_s')::int
FROM bronze_events
WHERE raw->>'squad' IS NOT NULL
  AND lower(trim(raw->>'status')) IN ('success', 'failed')
  AND raw->>'started_at' <> 'unknown'
ON CONFLICT (event_id) DO NOTHING
"""


def load(folder: Path = DATA) -> dict[str, int]:
    with connect() as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with open(folder / "squads.csv", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                conn.execute(
                    "INSERT INTO squads (squad, area, tribe)"
                    " VALUES (%(squad)s, %(area)s, %(tribe)s)"
                    " ON CONFLICT (squad) DO NOTHING",
                    row,
                )
        for file in sorted(folder.glob("deployments*.jsonl")):
            already = conn.execute(
                "SELECT count(*) FROM bronze_events WHERE source = %s", (file.name,)
            ).fetchone()[0]
            if already:
                continue  # this file is in bronze already
            with conn.cursor() as cur:
                lines = file.read_text(encoding="utf-8").splitlines()
                cur.executemany(
                    "INSERT INTO bronze_events (raw, source) VALUES (%s, %s)",
                    [(Jsonb(json.loads(line)), file.name) for line in lines],
                )
        conn.execute(CLEAN_SQL)
        counts = {
            t: conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            for t in ("squads", "bronze_events", "deployments")
        }
        conn.commit()
    return counts


if __name__ == "__main__":
    print(load())
