{{ 
    config(
        materialized='incremental',
        unique_key='date_key',
        on_schema_change='fail'
    )     
}}

WITH date_dimension AS (
    SELECT * FROM {{ ref('int_date_generate_dates') }}
),

fiscal_periods AS (
    {{ dbt_date.get_fiscal_periods(ref('int_date_generate_dates'), year_end_month=1, week_start_day=1, shift_year=1) }}
),

selected_dates AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['d.year_number', 'd.month_of_year', 'd.day_of_month']) }} AS date_key,
        CAST(d.year_number AS INTEGER) AS year,
        CAST(d.month_of_year AS INTEGER) AS month,
        CAST(d.day_of_month AS INTEGER) AS day
    FROM date_dimension AS d
    LEFT JOIN fiscal_periods AS fp
    ON d.date_day = fp.date_day
)

SELECT * FROM selected_dates