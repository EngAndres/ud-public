import json
from datetime import datetime, timedelta
from pathlib import Path

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

USGS_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
BRONZE_DIR = Path("/opt/airflow/datalake_bronze")


def extract_events(data_interval_start, data_interval_end, **_):
    """Call the USGS API for the time window of this run."""
    params = {
        "format": "geojson",
        "starttime": data_interval_start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": data_interval_end.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    response = requests.get(USGS_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_to_bronze(data_interval_start, ti, **_):
    """Write the raw API response to a timestamped JSON file."""
    payload = ti.xcom_pull(task_ids="extract")
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = data_interval_start.strftime("%Y%m%d_%H%M%S")
    path = BRONZE_DIR / f"earthquakes_{stamp}.json"
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file)
    return str(path)


with DAG(
    dag_id="earthquake_ingestion",
    description="Fetch USGS earthquakes daily at midnight (last 24 h) into the bronze layer",
    schedule="0 0 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=True,
    max_active_runs=4,
    default_args={"retries": 1, "retry_delay": timedelta(seconds=30)},
    tags=["bronze", "usgs"],
) as dag:
    extract = PythonOperator(task_id="extract", python_callable=extract_events)
    save = PythonOperator(task_id="save_to_bronze", python_callable=save_to_bronze)
    # Start curation as soon as this interval's raw file is saved.
    trigger_curation = TriggerDagRunOperator(
        task_id="trigger_curation",
        trigger_dag_id="earthquake_curation",
        logical_date="{{ data_interval_start.isoformat() }}",
        conf={
            "window_start": "{{ data_interval_start.isoformat() }}",
            "window_end": "{{ data_interval_end.isoformat() }}",
        },
        reset_dag_run=True,
    )

    extract >> save >> trigger_curation
