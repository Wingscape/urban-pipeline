FROM quay.io/astronomer/astro-runtime:12.7.0

WORKDIR '/usr/local/airflow'
COPY dbt-requirements.txt ./
RUN python -m virutalenv dbt_env && source dbt_env/bin/activate \
    && pip install --no-cache-dir -r dbt-requirements.txt && deactivate
