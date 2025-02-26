{{ 
    config(
        materialized='incremental',
        unique_key='location_key'
    )
}}

WITH data_location AS(
    SELECT
        'indonesia' AS country,
        'jakarta' AS capital_city
),

dim_location AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['country', 'capital_city']) }} AS location_key,
        country,
        capital_city
    FROM data_location
)

SELECT * FROM dim_location