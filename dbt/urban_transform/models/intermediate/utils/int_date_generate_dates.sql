{{ config(materialized='ephemeral') }}

{{ dbt_date.get_date_dimension('1998-12-30', '2026-01-01') }}