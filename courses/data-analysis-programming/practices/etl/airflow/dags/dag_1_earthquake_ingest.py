"""
DAG 1 - usgs_earthquake_ingest
==============================
Schedule : every 2 minutes  (*/2 * * * *)
Purpose  : Call the USGS Earthquake API and persist the raw response as a
           timestamped JSON file inside the datalake.

The file is intentionally kept raw so that DAG 2 can apply its own
curation/transformation logic independently.
"""

import json
import os
from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator
import requests

# -- Configuration -------------------------------------------------------------

USGS_EARTHQUAKE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
DATALAKE_RAW = "/opt/airflow/datalake/raw"

LOOKBACK_MINUTES = 2
MIN_MAGNITUDE = 0.0

# -- Task callable -------------------------------------------------------------

def _to_usgs_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def fetch_earthquakes(**context) -> str:
    """
    Fetch earthquake events from the USGS API for the last two minutes and
    write the raw JSON payload to datalake/raw/earthquake_<YYYYMMDD_HHMMSS>.json.

    Returns the absolute path of the written file.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=LOOKBACK_MINUTES)

    params = {
        "format": "geojson",
        "starttime": _to_usgs_timestamp(start_time),
        "endtime": _to_usgs_timestamp(end_time),
        "minmagnitude": MIN_MAGNITUDE,
        "orderby": "time",
        "limit": 20000,
    }

    response = requests.get(USGS_EARTHQUAKE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"earthquake_{timestamp}.json"
    filepath = os.path.join(DATALAKE_RAW, filename)

    os.makedirs(DATALAKE_RAW, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    feature_count = len(payload.get("features", []))
    print(f"[DAG 1] Fetched {feature_count} earthquake event(s) -> {filepath}")
    return filepath


# -- DAG definition ------------------------------------------------------------

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 3, 23),
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="dag_1_usgs_earthquake_ingest",
    description="Fetch USGS earthquake events and persist raw JSON to datalake every 2 min",
    default_args=default_args,
    schedule_interval="*/2 * * * *",
    catchup=False,
    tags=["usgs", "earthquake", "ingest", "datalake"],
) as dag:

    fetch_earthquakes_task = PythonOperator(
        task_id="fetch_earthquakes",
        python_callable=fetch_earthquakes,
    )
