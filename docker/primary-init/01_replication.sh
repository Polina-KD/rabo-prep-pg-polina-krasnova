#!/bin/bash
# Runs once, when the primary is created: a user for the replica, and permission to connect.
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<'SQL'
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SQL
echo "host replication replicator all scram-sha-256" >> "$PGDATA/pg_hba.conf"
