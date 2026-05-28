"""
DAG 3 - earthquake_postgres_to_parquet
======================================
Schedule : None - triggered by DAG 2 after each successful persistence run.
Purpose  : Read curated earthquake data from PostgreSQL, compute a multi-
                     dimensional summary, and persist it as Parquet files in
                     datalake/summary/.

Summary dimensions produced:
    1. magnitude_summary  - counts and magnitude stats by event type
    2. depth_summary      - depth stats grouped by event type
    3. strongest_10       - 10 strongest events ever recorded
    4. hourly_counts      - number of events per hour (trend over time)
    5. alert_summary      - counts by alert level and tsunami flag

Output: datalake/summary/earthquake_summary_<YYYYMMDD_HHMMSS>_*.parquet

Each summary is written as a separate Parquet file.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# -- Configuration -------------------------------------------------------------

DATALAKE_SUMMARY = "/opt/airflow/datalake/summary"
POSTGRES_CONN = "postgres_earthquake"

# -- Task callable -------------------------------------------------------------

def summarize_and_export(**context) -> list[str]:
    """
    Query PostgreSQL for each summary dimension, build a pandas DataFrame
    for each, and write them as Parquet files under datalake/summary/.

    Returns the list of written file paths (also stored in XCom for inspection).
    """
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(DATALAKE_SUMMARY)
    output_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[str] = []

    # 1. Magnitude summary by event type
    magnitude_sql = """
        SELECT
            COALESCE(event_type, 'unknown') AS event_type,
            COUNT(*)                        AS event_count,
            ROUND(AVG(magnitude)::numeric, 4) AS avg_magnitude,
            ROUND(MIN(magnitude)::numeric, 4) AS min_magnitude,
            ROUND(MAX(magnitude)::numeric, 4) AS max_magnitude
        FROM earthquakes
        GROUP BY COALESCE(event_type, 'unknown')
        ORDER BY event_count DESC, event_type;
    """
    df_magnitude = hook.get_pandas_df(magnitude_sql)
    path_magnitude = str(output_dir / f"earthquake_magnitude_summary_{timestamp}.parquet")
    df_magnitude.to_parquet(path_magnitude, index=False)
    written_files.append(path_magnitude)
    print(f"[DAG 3] Magnitude summary -> {path_magnitude}\n{df_magnitude}\n")

    # 2. Depth summary by event type
    depth_sql = """
        SELECT
            COALESCE(event_type, 'unknown') AS event_type,
            COUNT(*)                        AS event_count,
            ROUND(AVG(depth_km)::numeric, 4) AS avg_depth_km,
            ROUND(MIN(depth_km)::numeric, 4) AS min_depth_km,
            ROUND(MAX(depth_km)::numeric, 4) AS max_depth_km
        FROM earthquakes
        WHERE depth_km IS NOT NULL
        GROUP BY COALESCE(event_type, 'unknown')
        ORDER BY avg_depth_km ASC;
    """
    df_depth = hook.get_pandas_df(depth_sql)
    path_depth = str(output_dir / f"earthquake_depth_summary_{timestamp}.parquet")
    df_depth.to_parquet(path_depth, index=False)
    written_files.append(path_depth)
    print(f"[DAG 3] Depth summary -> {path_depth}\n{df_depth}\n")

    # 3. Strongest 10 events ever recorded
    top10_sql = """
        SELECT
            id,
            occurred_at,
            magnitude,
            magnitude_type,
            place,
            event_type,
            status,
            tsunami,
            alert,
            depth_km,
            longitude,
            latitude,
            title
        FROM earthquakes
        WHERE magnitude IS NOT NULL
        ORDER BY magnitude DESC, occurred_at DESC
        LIMIT 10;
    """
    df_top10 = hook.get_pandas_df(top10_sql)
    path_top10 = str(output_dir / f"earthquake_top10_strongest_{timestamp}.parquet")
    df_top10.to_parquet(path_top10, index=False)
    written_files.append(path_top10)
    print(f"[DAG 3] Top-10 strongest -> {path_top10}\n{df_top10}\n")

    # 4. Hourly trend
    hourly_sql = """
        SELECT
            date_trunc('hour', occurred_at) AS hour,
            COUNT(*)                       AS event_count,
            SUM(CASE WHEN tsunami THEN 1 ELSE 0 END) AS tsunami_count
        FROM earthquakes
        GROUP BY date_trunc('hour', occurred_at)
        ORDER BY hour;
    """
    df_hourly = hook.get_pandas_df(hourly_sql)
    path_hourly = str(output_dir / f"earthquake_hourly_counts_{timestamp}.parquet")
    df_hourly.to_parquet(path_hourly, index=False)
    written_files.append(path_hourly)
    print(f"[DAG 3] Hourly counts -> {path_hourly}\n{df_hourly}\n")

    # 5. Alert summary
    alert_sql = """
        SELECT
            COALESCE(alert, 'none') AS alert,
            tsunami,
            COUNT(*)                AS event_count,
            ROUND(AVG(magnitude)::numeric, 4) AS avg_magnitude
        FROM earthquakes
        GROUP BY COALESCE(alert, 'none'), tsunami
        ORDER BY event_count DESC, alert;
    """
    df_alert = hook.get_pandas_df(alert_sql)
    path_alert = str(output_dir / f"earthquake_alert_summary_{timestamp}.parquet")
    df_alert.to_parquet(path_alert, index=False)
    written_files.append(path_alert)
    print(f"[DAG 3] Alert summary -> {path_alert}\n{df_alert}\n")

    print(f"[DAG 3] Done - wrote {len(written_files)} Parquet file(s).")
    return written_files


# DAG definition
default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 3, 23),
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="dag_3_earthquake_postgres_to_parquet",
    description="Summarise earthquake data from PostgreSQL and persist as Parquet (triggered by DAG 2)",
    default_args=default_args,
    schedule_interval=None,   # Triggered only — never runs on its own schedule
    catchup=False,
    tags=["usgs", "earthquake", "parquet", "summary"],
) as dag:

    summarize_task = PythonOperator(
        task_id="summarize_and_export",
        python_callable=summarize_and_export,
    )
