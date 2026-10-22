from datetime import datetime
from pathlib import Path

import polars as pl
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.external_task import ExternalTaskSensor

GOLD_DIR = Path("/opt/airflow/datalake_gold")
CONN_ID = "postgres_etl"
QUERY = """
SELECT event_id, event_time, magnitude, depth_km
FROM earthquakes_curated
WHERE event_time >= NOW() - INTERVAL '24 hours';
"""


def compute_statistics(data_interval_end, **_):
    """Aggregate the last 24 hours of events and write one Parquet file."""
    pandas_df = PostgresHook(postgres_conn_id=CONN_ID).get_pandas_df(QUERY)
    events = pl.from_pandas(pandas_df)

    stats = events.select(
        pl.len().alias("event_count"),
        pl.col("magnitude").mean().alias("avg_magnitude"),
        pl.col("magnitude").max().alias("max_magnitude"),
        pl.col("depth_km").mean().alias("avg_depth_km"),
    ).with_columns(
        pl.lit(data_interval_end.replace(tzinfo=None)).alias("snapshot_end"),
    )

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    stamp = data_interval_end.strftime("%Y%m%d_%H%M%S")
    path = GOLD_DIR / f"earthquake_stats_{stamp}.parquet"
    stats.write_parquet(path)
    print(stats)
    return str(path)


with DAG(
    dag_id="earthquake_analysis",
    description="Compute 24-hour earthquake statistics and save them as Parquet",
    schedule="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 1},
    tags=["gold", "analysis"],
) as dag:
    wait_for_curation = ExternalTaskSensor(
        task_id="wait_for_curation",
        external_dag_id="earthquake_curation",
        external_task_id="curate_and_load",
        mode="reschedule",
        timeout=600,
    )
    compute = PythonOperator(task_id="compute_statistics", python_callable=compute_statistics)

    wait_for_curation >> compute
