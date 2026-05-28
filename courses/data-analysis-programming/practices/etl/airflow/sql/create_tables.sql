-- Ensure the schema exists and scope all objects to it.
CREATE SCHEMA IF NOT EXISTS ud;
SET search_path TO ud;

-- Tracks every raw JSON file ingested by DAG 1.
-- DAG 2 queries this table to know which files are still pending.
CREATE TABLE IF NOT EXISTS processed_files (
    filename TEXT PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- One row per unique earthquake event returned by the USGS API.
-- Upserted on each DAG 2 run; keyed on the event id.
CREATE TABLE IF NOT EXISTS earthquakes (
    id TEXT PRIMARY KEY,
    occurred_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    magnitude DOUBLE PRECISION,
    magnitude_type TEXT,
    place TEXT,
    event_type TEXT,
    status TEXT,
    tsunami BOOLEAN NOT NULL DEFAULT FALSE,
    felt INTEGER,
    cdi DOUBLE PRECISION,
    mmi DOUBLE PRECISION,
    alert TEXT,
    significance    INTEGER,
    network TEXT,
    code TEXT,
    url TEXT,
    detail TEXT,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    depth_km  DOUBLE PRECISION,
    nst INTEGER,
    dmin DOUBLE PRECISION,
    rms DOUBLE PRECISION,
    gap DOUBLE PRECISION,
    sources TEXT,
    types TEXT,
    title TEXT,
    raw_json JSONB,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
