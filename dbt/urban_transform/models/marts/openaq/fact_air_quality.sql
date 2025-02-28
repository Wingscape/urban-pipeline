{{ config(materialized='table') }}

WITH fetched_openaq AS (
    SELECT * FROM {{ ref('int_openaq_fetch_data') }}
),

fact_air AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['pull_date', 'key', "'openaq'"]) }} AS air_key,
        {{ dbt_utils.generate_surrogate_key(['YEAR(pull_date)', 'MONTH(pull_date)', 'DAY(pull_date)']) }} AS date_key,
        {{ dbt_utils.generate_surrogate_key(["'openaq'"]) }} AS source_key,
        {{ dbt_utils.generate_surrogate_key(["'indonesia'", "'jakarta'"]) }} AS location_key,
        {{ dbt_utils.generate_surrogate_key(["'pm25'", "'µg/m³'"]) }} AS parameter_key,
        {{ dbt_utils.generate_surrogate_key(['key']) }} AS agg_type_key,
        value AS agg_value,
        air_value
    FROM fetched_openaq
)

SELECT * FROM fact_air
