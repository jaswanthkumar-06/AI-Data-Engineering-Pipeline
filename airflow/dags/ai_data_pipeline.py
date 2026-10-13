
from datetime import datetime
import os
import subprocess
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


PROJECT = "/opt/airflow/project"
DBT_PROJECT = f"{PROJECT}/dbt/ai_data_pipeline"


def run_ai_sentiment():
    subprocess.run(
        [
            sys.executable,
            f"{PROJECT}/ai/review_insights.py",
        ],
        check=True,
        cwd=PROJECT,
    )


def load_ai_results():
    import psycopg2

    csv_path = f"{PROJECT}/data/processed/review_sentiment.csv"

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Sentiment output CSV not found: {csv_path}"
        )

    connection = psycopg2.connect(
        host="postgres",
        port=5432,
        database="ai_data_pipeline",
        user="postgres",
        password="postgres",
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS ai;

                CREATE TABLE IF NOT EXISTS ai.review_sentiment (
                    review_id INTEGER,
                    sentiment VARCHAR(20),
                    sentiment_score DOUBLE PRECISION,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("TRUNCATE TABLE ai.review_sentiment;")

            with open(csv_path, "r", encoding="utf-8") as file:
                cursor.copy_expert(
                    """
                    COPY ai.review_sentiment
                    FROM STDIN
                    WITH (FORMAT CSV, HEADER TRUE)
                    """,
                    file,
                )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


with DAG(
    dag_id="ai_data_engineering_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "ai", "dbt"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command=(
            f"cd {PROJECT} && "
            f"{sys.executable} ingestion/generate_data.py"
        ),
    )

    ai_sentiment = PythonOperator(
        task_id="ai_sentiment_analysis",
        python_callable=run_ai_sentiment,
    )

    load_ai = PythonOperator(
        task_id="load_ai_results",
        python_callable=load_ai_results,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_PROJECT} && "
            f"{sys.executable} -m dbt.cli.main build --profiles-dir ."
        ),
        env={
            "DBT_HOST": "postgres",
        },
    )

    generate_data >> ai_sentiment >> load_ai >> dbt_build
