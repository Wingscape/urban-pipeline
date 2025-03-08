{{ 
    config(
        materialized='incremental',
        unique_key='agg_type_key',
        on_schema_change='fail'
    )
}}

WITH fetched_openaq AS (
    SELECT * FROM {{ ref('int_openaq_fetch_data') }}
),

dim_agg_type AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['key']) }} AS agg_type_key,
        key AS name
    FROM fetched_openaq
)

SELECT * FROM dim_agg_type
