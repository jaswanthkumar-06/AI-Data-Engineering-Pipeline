FROM apache/airflow:2.10.5-python3.11

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    psycopg2-binary \
    dbt-core \
    dbt-postgres