-- Part B: the query of the dashboard. Run it with EXPLAIN ANALYZE before and after the index.
EXPLAIN ANALYZE
SELECT count(*)
FROM deployments_big
WHERE squad = 'Metron'
  AND started_at >= '2026-11-16' AND started_at < '2026-11-23';
