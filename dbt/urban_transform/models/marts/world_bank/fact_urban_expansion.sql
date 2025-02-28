{{ config(materialized='table') }}

WITH raw_world_bank AS (
    SELECT * FROM {{ ref('stg_raw__world_banks') }}
),

fact_urban AS (
    SELECT 
        {{ dbt_utils.generate_surrogate_key(['raw_date::string', "'world bank'"]) }} AS urban_key,
        {{ dbt_utils.generate_surrogate_key(['raw_date::string', "'1'", "'1'"]) }} AS date_key,
        {{ dbt_utils.generate_surrogate_key(["'world bank'"]) }} AS source_key,
        {{ dbt_utils.generate_surrogate_key(["'indonesia'", "'jakarta'"]) }} AS location_key,
        "'total population'" AS total_population,
        "'total urban population'" AS urban_population,
        "'total rural population'" AS rural_population,
        "'largest city population'" AS largest_city_population,
        "'urban population percentage'" AS urban_population_percent,
        "'rural population percentage'" AS rural_population_percent,
        "'largest city population percentage'" AS largest_city_population_percent,
        "'air pollution mean annual exposure'" AS air_pollution_pm25
    FROM (
        SELECT 
            raw_flatten.value:date AS raw_date,
            raw_world_bank.context AS context, 
            raw_flatten.value:value AS raw_value
        FROM 
            raw_world_bank, 
            LATERAL FLATTEN(INPUT => raw_world_bank.raw_data[1]) AS raw_flatten 
    ) PIVOT (
        MIN(raw_value) FOR context IN (
            'total population',
            'total urban population',
            'total rural population',
            'largest city population',
            'urban population percentage',
            'rural population percentage',
            'largest city population percentage',
            'air pollution mean annual exposure'
        )
    ) ORDER BY raw_date
)

SELECT * FROM fact_urban
