WITH data_source AS (
    SELECT * FROM {{ source('raw', 'data_source') }}
),

raw_openaq AS (
    SELECT
        id AS raw_id,
        name AS raw_source_name,
        type AS raw_type,
        context,
        raw_data,
        pull_date,
        pull_timestamp
    FROM data_source WHERE name = 'openaq' AND pull_date = CURRENT_DATE
)

SELECT * FROM raw_openaq
