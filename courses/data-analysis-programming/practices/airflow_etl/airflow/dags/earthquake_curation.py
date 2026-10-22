import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

BRONZE_DIR = Path("/opt/airflow/datalake_bronze")
CONN_ID = "postgres_etl"
FILE_PATTERN = re.compile(r"earthquakes_(\d{8}_\d{6})\.json$")
COLUMNS = [
    "event_id", "event_time", "magnitude", "place",
    "latitude", "longitude", "depth_km", "event_type",
]

DDL = """
CREATE TABLE IF NOT EXISTS earthquakes_curated (
    event_id    TEXT PRIMARY KEY,
    event_time  TIMESTAMPTZ NOT NULL,
    magnitude   DOUBLE PRECISION NOT NULL,
    place       TEXT,
    latitude    DOUBLE PRECISION,
    longitude   DOUBLE PRECISION,
    depth_km    DOUBLE PRECISION,
    event_type  TEXT
);
"""


def create_table():
    """Create the curated table if it does not exist yet (safe to run repeatedly)."""
    PostgresHook(postgres_conn_id=CONN_ID).run(DDL)


def read_bronze_window(window_start, window_end):
    """Return the flattened features from bronze files stamped inside [start, end)."""
    records = []
    for path in sorted(BRONZE_DIR.glob("earthquakes_*.json")):
        match = FILE_PATTERN.search(path.name)
        if not match:
            continue
        file_time = datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
        if not window_start <= file_time < window_end:
            continue
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


def curate_and_load(data_interval_start, data_interval_end, **_):
    """Clean the window's records and upsert them into PostgreSQL."""
    window_start = data_interval_start.replace(tzinfo=None)
    window_end = data_interval_end.replace(tzinfo=None)
    df = pd.DataFrame(read_bronze_window(window_start, window_end))

    if df.empty:
        print("No events in this window; nothing to load.")
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

    # Idempotent load: rows with an existing event_id are updated, not duplicated.
    PostgresHook(postgres_conn_id=CONN_ID).insert_rows(
        table="earthquakes_curated",
        rows=rows,
        target_fields=COLUMNS,
        replace=True,
        replace_index="event_id",
    )
    print(f"Loaded {len(rows)} events.")
    return len(rows)


with DAG(
    dag_id="earthquake_curation",
    description="Curate bronze earthquake files and load them into PostgreSQL",
    schedule="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 1},
    tags=["silver", "postgres"],
) as dag:
    prepare = PythonOperator(task_id="create_table", python_callable=create_table)
    curate = PythonOperator(task_id="curate_and_load", python_callable=curate_and_load)

    prepare >> curate
