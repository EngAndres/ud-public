touch docker-compose.yml
touch .env
echo "AIRFLOW_UID=$(id -u)" > .env

mkdir datalake_bronze
mkdir datalake_gold

mkdir init-db
cd init-db
touch 01-create-etl-database.sql
cd ../

mkdir airflow 
cd airflow
mkdir dags 
cd dags
touch earthquake_ingestion.py
touch earthquake_curation.py
touch earthquake_analysis.py
