WITH source AS (
    SELECT * FROM {{ source('raw', 'data_source') }}
),

renamed AS (
    SELECT
        id AS raw_id,
        name AS raw_name,
        type AS raw_type,
        context,
        raw_data,
        pull_date,
        pull_timestamp
    FROM source WHERE name = 'openaq' AND pull_date = CURRENT_DATE
)

SELECT * FROM renamed
