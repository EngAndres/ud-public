"""
DAG 2 - earthquake_json_to_postgres
===================================
Schedule : every 20 minutes  (*/20 * * * *)
Purpose  : Pick up every unprocessed JSON file produced by DAG 1, curate and
           normalise the earthquake events, upsert them into PostgreSQL,
           then trigger DAG 3 for the summary step.

Task chain:
    create_tables  (PostgresOperator)
        -> curate_pending_files  (PythonOperator)  -> pushes curated records
           via XCom
        -> persist_to_postgres  (PythonOperator)   -> upserts + marks files
           as processed
        -> trigger_dag3  (TriggerDagRunOperator)

Curation rules applied in curate_pending_files:
  - Strip whitespace from string fields
  - Cast numeric fields to float or int when available
  - Convert epoch milliseconds to UTC timestamps
  - Deduplicate earthquakes by id within the same batch
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from psycopg2.extras import Json

# -- Configuration -------------------------------------------------------------

DATALAKE_RAW = "/opt/airflow/datalake/raw"
POSTGRES_CONN = "postgres_earthquake"
SQL_DIR = "/opt/airflow/sql"

def _to_utc_datetime(value):
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def curate_pending_files(**context) -> dict:
    """
    1. List all *.json files inside DATALAKE_RAW.
    2. Query processed_files to find which ones are already done.
    3. For each pending file: read, flatten the nested GeoJSON structure,
       apply curation rules, accumulate records.
    4. Push a dict with keys 'earthquakes' and 'filenames' to XCom so the next
       task can persist them.
    """
    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN)

    # Files already processed
    processed = {
        row[0]
        for row in hook.get_records("SELECT filename FROM processed_files;")
    }

    raw_dir = Path(DATALAKE_RAW)
    pending_files = sorted(f.name for f in raw_dir.glob("earthquake_*.json") if f.name not in processed)

    if not pending_files:
        print("[DAG 2 / curate] No pending files found — nothing to do.")
        return {"earthquakes": [], "filenames": []}

    print(f"[DAG 2 / curate] Processing {len(pending_files)} file(s): {pending_files}")

    earthquakes_map: dict[str, tuple] = {}

    for filename in pending_files:
        filepath = raw_dir / filename
        with open(filepath, encoding="utf-8") as f:
            payload = json.load(f)

        for feature in payload.get("features", []):
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coordinates = geometry.get("coordinates") or []

            earthquake_id = str(feature.get("id", "")).strip()
            if not earthquake_id:
                continue

            earthquakes_map[earthquake_id] = (
                earthquake_id,
                _to_utc_datetime(properties.get("time")),
                _to_utc_datetime(properties.get("updated")),
                float(properties["mag"]) if properties.get("mag") is not None else None,
                str(properties.get("magType", "")).strip() or None,
                str(properties.get("place", "")).strip() or None,
                str(properties.get("type", "")).strip() or None,
                str(properties.get("status", "")).strip() or None,
                bool(properties.get("tsunami", 0)),
                int(properties["felt"]) if properties.get("felt") is not None else None,
                float(properties["cdi"]) if properties.get("cdi") is not None else None,
                float(properties["mmi"]) if properties.get("mmi") is not None else None,
                str(properties.get("alert", "")).strip() or None,
                int(properties["sig"]) if properties.get("sig") is not None else None,
                str(properties.get("net", "")).strip() or None,
                str(properties.get("code", "")).strip() or None,
                str(properties.get("url", "")).strip() or None,
                str(properties.get("detail", "")).strip() or None,
                float(coordinates[0]) if len(coordinates) > 0 and coordinates[0] is not None else None,
                float(coordinates[1]) if len(coordinates) > 1 and coordinates[1] is not None else None,
                float(coordinates[2]) if len(coordinates) > 2 and coordinates[2] is not None else None,
                int(properties["nst"]) if properties.get("nst") is not None else None,
                float(properties["dmin"]) if properties.get("dmin") is not None else None,
                float(properties["rms"]) if properties.get("rms") is not None else None,
                float(properties["gap"]) if properties.get("gap") is not None else None,
                str(properties.get("sources", "")).strip() or None,
                str(properties.get("types", "")).strip() or None,
                str(properties.get("title", "")).strip() or None,
                feature,
            )

    curated = {
        "earthquakes": list(earthquakes_map.values()),
        "filenames": pending_files,
    }
    print(
        f"[DAG 2 / curate] Curated "
        f"{len(curated['earthquakes'])} earthquake event(s)."
    )
    return curated


def persist_to_postgres(**context) -> None:
    """
    Pull curated records from XCom, upsert into PostgreSQL, and mark each
    source file as processed.

    Upsert strategy:
            - earthquakes     : ON CONFLICT (id) DO UPDATE - refresh event fields
            - processed_files : ON CONFLICT (filename) DO NOTHING
    """
    ti = context["ti"]
    curated: dict = ti.xcom_pull(task_ids="curate_pending_files")

    if not curated or not curated.get("filenames"):
        print("[DAG 2 / persist] No data to persist.")
        return

    hook = PostgresHook(postgres_conn_id=POSTGRES_CONN)
    conn = hook.get_conn()
    cursor = conn.cursor()

    try:
        earthquake_sql = """
            INSERT INTO earthquakes
                (
                    id,
                    occurred_at,
                    updated_at,
                    magnitude,
                    magnitude_type,
                    place,
                    event_type,
                    status,
                    tsunami,
                    felt,
                    cdi,
                    mmi,
                    alert,
                    significance,
                    network,
                    code,
                    url,
                    detail,
                    longitude,
                    latitude,
                    depth_km,
                    nst,
                    dmin,
                    rms,
                    gap,
                    sources,
                    types,
                    title,
                    raw_json,
                    ingested_at
                )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (id) DO UPDATE SET
                occurred_at    = EXCLUDED.occurred_at,
                updated_at     = EXCLUDED.updated_at,
                magnitude      = EXCLUDED.magnitude,
                magnitude_type = EXCLUDED.magnitude_type,
                place          = EXCLUDED.place,
                event_type     = EXCLUDED.event_type,
                status         = EXCLUDED.status,
                tsunami        = EXCLUDED.tsunami,
                felt           = EXCLUDED.felt,
                cdi            = EXCLUDED.cdi,
                mmi            = EXCLUDED.mmi,
                alert          = EXCLUDED.alert,
                significance   = EXCLUDED.significance,
                network        = EXCLUDED.network,
                code           = EXCLUDED.code,
                url            = EXCLUDED.url,
                detail         = EXCLUDED.detail,
                longitude      = EXCLUDED.longitude,
                latitude       = EXCLUDED.latitude,
                depth_km       = EXCLUDED.depth_km,
                nst            = EXCLUDED.nst,
                dmin           = EXCLUDED.dmin,
                rms            = EXCLUDED.rms,
                gap            = EXCLUDED.gap,
                sources        = EXCLUDED.sources,
                types          = EXCLUDED.types,
                title          = EXCLUDED.title,
                raw_json       = EXCLUDED.raw_json,
                ingested_at    = NOW();
        """
        rows = [t[:28] + [Json(t[28])] for t in curated["earthquakes"]]
        cursor.executemany(earthquake_sql, rows)
        print(f"[DAG 2 / persist] Upserted {cursor.rowcount} earthquake rows.")

        # Mark files as processed
        for filename in curated["filenames"]:
            cursor.execute(
                """
                INSERT INTO processed_files (filename, processed_at)
                VALUES (%s, NOW())
                ON CONFLICT (filename) DO NOTHING;
                """,
                (filename,),
            )

        conn.commit()
        print(
            f"[DAG 2 / persist] Committed. "
            f"Marked {len(curated['filenames'])} file(s) as processed."
        )
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


# DAG definition
default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 3, 23),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_2_earthquake_json_to_postgres",
    description="Curate pending earthquake JSON files and upsert into PostgreSQL every 20 min",
    default_args=default_args,
    schedule_interval="*/20 * * * *",
    catchup=False,
    # Allows PostgresOperator to resolve SQL files relative to /opt/airflow/sql/
    template_searchpath=["/opt/airflow/sql"],
    tags=["usgs", "earthquake", "postgres", "etl"],
) as dag:

    # Task 1: Ensure schema exists
    create_tables = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id=POSTGRES_CONN,
        sql="create_tables.sql",
    )

    # Task 2: Read + curate all pending JSON files
    curate_task = PythonOperator(
        task_id="curate_pending_files",
        python_callable=curate_pending_files,
    )

    # Task 3: Persist curated data into PostgreSQL
    persist_task = PythonOperator(
        task_id="persist_to_postgres",
        python_callable=persist_to_postgres,
    )

    # Task 4: Trigger DAG 3
    trigger_dag3 = TriggerDagRunOperator(
        task_id="trigger_dag3",
        trigger_dag_id="dag_3_earthquake_postgres_to_parquet",
        wait_for_completion=False,
        reset_dag_run=True,
    )

    create_tables >> curate_task >> persist_task >> trigger_dag3
