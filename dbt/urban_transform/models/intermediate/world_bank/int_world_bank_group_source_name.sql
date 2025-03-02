WITH raw_world_bank AS (
    SELECT * FROM {{ ref('stg_raw__world_banks') }}
),

group_world_bank AS (
    SELECT
        raw_source_name
    FROM raw_world_bank
    GROUP BY raw_source_name
)

SELECT * FROM group_world_bank