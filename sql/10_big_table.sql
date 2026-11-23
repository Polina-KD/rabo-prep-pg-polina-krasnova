-- Part B: a big table with 1,000,000 invented deployments, to see what an index does.
-- Run: docker compose exec primary psql -U postgres -d delivery -f /sql/10_big_table.sql
SELECT setseed(0.42);
DROP TABLE IF EXISTS deployments_big;
CREATE TABLE deployments_big AS
SELECT g AS id,
       (ARRAY['Metron','Atlas','Phoenix','Orion','Nova','Vega','Lyra','Draco'])[1 + floor(random() * 8)::int] AS squad,
       (ARRAY['prod','acc','test'])[1 + floor(random() * 3)::int] AS environment,
       CASE WHEN random() < 0.9 THEN 'success' ELSE 'failed' END AS status,
       timestamptz '2025-01-01 00:00+00' + random() * interval '700 days' AS started_at
FROM generate_series(1, 1000000) AS g;
ANALYZE deployments_big;
SELECT count(*) AS rows FROM deployments_big;
