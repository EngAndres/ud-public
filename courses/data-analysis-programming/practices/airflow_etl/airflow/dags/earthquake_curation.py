import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import execute_values

BRONZE_DIR = Path("/opt/airflow/datalake_bronze")
CONN_ID = "postgres_etl"
FILE_PATTERN = re.compile(r"earthquakes_(\d{8}_\d{6})\.json$")
COLUMNS = [
    "event_id", "event_time", "magnitude", "place",
    "latitude", "longitude", "depth_km", "event_type",
]
DDL = """
CREATE TABLE IF NOT EXISTS earthquakes_zipper (
    event_id    TEXT NOT NULL,
    event_time  TIMESTAMPTZ NOT NULL,
    magnitude   DOUBLE PRECISION NOT NULL,
    place       TEXT,
    latitude    DOUBLE PRECISION,
    longitude   DOUBLE PRECISION,
    depth_km    DOUBLE PRECISION,
    event_type  TEXT,
    valid_from  TIMESTAMPTZ NOT NULL,
    valid_to    TIMESTAMPTZ,
    is_current  BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS earthquakes_zipper_current_idx
    ON earthquakes_zipper (event_id) WHERE is_current;
"""

CREATE_STAGING = """
CREATE TEMP TABLE staging (
    event_id    TEXT,
    event_time  TIMESTAMPTZ,
    magnitude   DOUBLE PRECISION,
    place       TEXT,
    latitude    DOUBLE PRECISION,
    longitude   DOUBLE PRECISION,
    depth_km    DOUBLE PRECISION,
    event_type  TEXT
) ON COMMIT DROP;
"""

# Close the current version of every event whose tracked values changed.
CLOSE_CHANGED = """
UPDATE earthquakes_zipper AS z
SET valid_to = %(window_end)s, is_current = FALSE
FROM staging AS s
WHERE z.event_id = s.event_id
  AND z.is_current
  AND (z.event_time, z.magnitude, z.place, z.latitude, z.longitude, z.depth_km, z.event_type)
      IS DISTINCT FROM
      (s.event_time, s.magnitude, s.place, s.latitude, s.longitude, s.depth_km, s.event_type);
"""

# Open a new version for events that are new or whose current version was just closed.
INSERT_NEW_VERSIONS = """
INSERT INTO earthquakes_zipper (
    event_id, event_time, magnitude, place, latitude, longitude, depth_km, event_type,
    valid_from, valid_to, is_current
)
SELECT s.event_id, s.event_time, s.magnitude, s.place, s.latitude, s.longitude,
       s.depth_km, s.event_type, %(window_end)s, NULL, TRUE
FROM staging AS s
LEFT JOIN earthquakes_zipper AS z ON z.event_id = s.event_id AND z.is_current
WHERE z.event_id IS NULL;
"""


def create_table():
    """Create the zipper table if it does not exist yet (safe to run repeatedly)."""
    PostgresHook(postgres_conn_id=CONN_ID).run(DDL)


def bronze_files_in_window(window_start, window_end):
    """Return the bronze files stamped inside [start, end)."""
    files = []
    for path in sorted(BRONZE_DIR.glob("earthquakes_*.json")):
        match = FILE_PATTERN.search(path.name)
        if not match:
            continue
        file_time = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
        if window_start <= file_time < window_end:
            files.append(path)
    return files


def read_bronze_files(paths):
    """Return the flattened features from the given bronze files."""
    records = []
    for path in paths:
        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
        for feature in payload.get("features", []):
            props = feature.get("properties") or {}
            lon, lat, depth = (feature.get("geometry") or {}).get(
                "coordinates", [None, None, None]
            )
            records.append({
                "event_id": feature.get("id"),
                "event_time": props.get("time"),  # epoch milliseconds
                "magnitude": props.get("mag"),
                "place": props.get("place"),
                "latitude": lat,
                "longitude": lon,
                "depth_km": depth,
                "event_type": props.get("type"),
            })
    return records


def load_zipper(rows, window_end):
    """Apply the window's rows to the zipper table in one transaction."""
    conn = PostgresHook(postgres_conn_id=CONN_ID).get_conn()
    try:
        with conn:  # commits on success, rolls back on error
            with conn.cursor() as cur:
                cur.execute(CREATE_STAGING)
                execute_values(cur, f"INSERT INTO staging ({', '.join(COLUMNS)}) VALUES %s", rows)
                cur.execute(CLOSE_CHANGED, {"window_end": window_end})
                cur.execute(INSERT_NEW_VERSIONS, {"window_end": window_end})
                return cur.rowcount
    finally:
        conn.close()


def curate_and_load(dag_run, **_):
    """Clean the window's records and apply them to the zipper table."""
    window_start = datetime.fromisoformat(dag_run.conf["window_start"])
    window_end = datetime.fromisoformat(dag_run.conf["window_end"])

    files = bronze_files_in_window(window_start.replace(tzinfo=None), window_end.replace(tzinfo=None))
    if not files:
        raise AirflowFailException(f"No bronze file found for window {window_start} to {window_end}.")

    df = pd.DataFrame(read_bronze_files(files))
    if df.empty:
        print("Bronze files contain no events for this window; nothing to load.")
        return 0

    # Validation: drop rows without an identifier, magnitude, or time.
    df = df.dropna(subset=["event_id", "magnitude", "event_time"])
    # Deduplication: the same event can appear in overlapping API responses.
    df = df.drop_duplicates(subset="event_id", keep="last")
    # Standardization: timestamps as UTC datetimes, text trimmed, missing places labeled.
    df["event_time"] = pd.to_datetime(df["event_time"], unit="ms", utc=True)
    df["place"] = df["place"].fillna("unknown").str.strip()

    rows = [
        tuple(
            None if pd.isna(value)
            else value.to_pydatetime() if isinstance(value, pd.Timestamp)
            else value
            for value in row
        )
        for row in df[COLUMNS].itertuples(index=False, name=None)
    ]

    load_zipper(rows, window_end)
    print(f"Processed {len(rows)} events for {window_start} to {window_end}.")
    return len(rows)


with DAG(
    dag_id="earthquake_curation",
    description="Curate bronze earthquake files into a PostgreSQL zipper (history) table",
    schedule=None,  # triggered by earthquake_ingestion after each raw file is saved
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,  # apply versions in order
    default_args={"retries": 1},
    tags=["silver", "postgres"],
) as dag:
    prepare = PythonOperator(task_id="create_table", python_callable=create_table)
    curate = PythonOperator(task_id="curate_and_load", python_callable=curate_and_load)

    prepare >> curate
