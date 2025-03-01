{{ 
    config(
        materialized='incremental',
        unique_key='source_key',
        on_schema_change='fail'
    )
}}

WITH grouped_world_bank_source_name AS (
    SELECT * FROM {{ ref('int_world_bank_group_source_name') }}
),

grouped_openaq_source_name AS (
    SELECT * FROM {{ ref('int_openaq_group_source_name') }}
),

union_grouped_source_name AS (
    SELECT * FROM grouped_world_bank_source_name
    UNION
    SELECT * FROM grouped_openaq_source_name
),

dim_source AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['raw_source_name']) }} AS source_key,
        raw_source_name AS name
    FROM union_grouped_source_name
)

SELECT * FROM dim_source
