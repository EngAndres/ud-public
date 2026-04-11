CREATE TABLE IF NOT EXISTS processed_files(
    filename TEXT PRIMARY KEY,
    processed_at TIMESTAMP NOT NULL DEFAULT NOW()
) 

CREATE TABLE IF NOT EXISTS earthquakes (
    id VARCHAR(50) PRIMARY KEY,
    magnitude DOUBLE PRECISION,
    place VARCHAR, 
    status VARCHAR,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)