from datetime import datetime
from pathlib import Path

import polars as pl
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

GOLD_DIR = Path("/opt/airflow/datalake_gold")
CONN_ID = "postgres_etl"
QUERY = """
SELECT event_id, event_time, magnitude, depth_km
FROM earthquakes_zipper
WHERE is_current
  AND event_time >= %(week_start)s
  AND event_time < %(week_end)s;
"""


def compute_statistics(data_interval_end, **_):
    """Aggregate the 7 days ending at Monday 00:00 and write one Parquet file."""
    week_end = data_interval_end.start_of("day")
    week_start = week_end.subtract(days=7)

    pandas_df = PostgresHook(postgres_conn_id=CONN_ID).get_pandas_df(
        QUERY, parameters={"week_start": week_start, "week_end": week_end}
    )
    pandas_df = pandas_df.astype({"magnitude": "float64", "depth_km": "float64"})
    events = pl.from_pandas(pandas_df)

    stats = events.select(
        pl.len().alias("event_count"),
        pl.col("magnitude").mean().alias("avg_magnitude"),
        pl.col("magnitude").max().alias("max_magnitude"),
        pl.col("depth_km").mean().alias("avg_depth_km"),
    ).with_columns(
        pl.lit(week_start.replace(tzinfo=None)).alias("week_start"),
        pl.lit(week_end.replace(tzinfo=None)).alias("week_end"),
    )

    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    stamp = week_end.strftime("%Y%m%d")
    path = GOLD_DIR / f"earthquake_stats_{stamp}.parquet"
    stats.write_parquet(path)
    print(stats)
    return str(path)


with DAG(
    dag_id="earthquake_analysis",
    description="Compute weekly earthquake statistics from the zipper table and save them as Parquet",
    schedule="0 3 * * 1",  # Mondays at 03:00, after the week's daily runs have finished
    start_date=datetime(2026, 1, 1),
    catchup=True,
    default_args={"retries": 1},
    tags=["gold", "analysis"],
) as dag:
    compute = PythonOperator(task_id="compute_statistics", python_callable=compute_statistics)
