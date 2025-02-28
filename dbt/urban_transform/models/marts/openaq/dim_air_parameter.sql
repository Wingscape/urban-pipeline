{{ 
    config(
        materialized='incremental',
        unique_key='parameter_key'
    )
}}

WITH data_parameter AS(
    SELECT
        'pm25' AS name,
        'µg/m³' AS units
),

dim_air_parameter AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['name', 'units']) }} AS parameter_key,
        name,
        units
    FROM data_parameter
)

SELECT * FROM dim_air_parameter