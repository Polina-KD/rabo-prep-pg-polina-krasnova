-- Part B: a partitioned table: one partition per month (2026 only, to keep it short).
DROP TABLE IF EXISTS deployments_part;
CREATE TABLE deployments_part (
    id bigint, squad text, environment text, status text, started_at timestamptz NOT NULL
) PARTITION BY RANGE (started_at);

DO $$
DECLARE m date := date '2026-01-01';
BEGIN
    WHILE m < date '2027-01-01' LOOP
        EXECUTE format(
            'CREATE TABLE deployments_part_%s PARTITION OF deployments_part FOR VALUES FROM (%L) TO (%L)',
            to_char(m, 'YYYY_MM'), m, (m + interval '1 month')::date);
        m := (m + interval '1 month')::date;
    END LOOP;
END $$;

INSERT INTO deployments_part
SELECT id, squad, environment, status, started_at FROM deployments_big
WHERE started_at >= '2026-01-01' AND started_at < '2027-01-01';
ANALYZE deployments_part;

-- Look at the plan: only the partition of November is read (partition pruning).
EXPLAIN SELECT count(*) FROM deployments_part
WHERE started_at >= '2026-11-01' AND started_at < '2026-12-01';
