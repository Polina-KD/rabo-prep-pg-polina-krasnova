DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles
        WHERE rolname = 'dashboard_reader'
    ) THEN
        CREATE ROLE dashboard_reader NOLOGIN;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles
        WHERE rolname = 'app_writer'
    ) THEN
        CREATE ROLE app_writer NOLOGIN;
    END IF;
END
$$;

GRANT SELECT ON TABLE squads, deployments
TO dashboard_reader;

GRANT SELECT, INSERT, UPDATE
ON TABLE squads, deployments, bronze_events
TO app_writer;

GRANT USAGE, SELECT
ON SEQUENCE bronze_events_id_seq
TO app_writer;