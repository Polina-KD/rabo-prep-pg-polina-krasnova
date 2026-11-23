-- V001: the first tables. A migration runs once; the table schema_migrations remembers it.
CREATE TABLE bronze_events (
    id         bigserial PRIMARY KEY,
    raw        jsonb       NOT NULL,          -- the event exactly as received
    source     text        NOT NULL,          -- the file it came from
    loaded_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE squads (
    squad text PRIMARY KEY,
    area  text NOT NULL,
    tribe text NOT NULL
);

CREATE TABLE deployments (
    event_id    text        PRIMARY KEY,
    squad       text        NOT NULL REFERENCES squads (squad),
    service     text,
    environment text        NOT NULL CHECK (environment IN ('prod', 'acc', 'test')),
    status      text        NOT NULL CHECK (status IN ('success', 'failed')),
    started_at  timestamptz NOT NULL,
    duration_s  integer
);
