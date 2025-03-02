WITH raw_openaqs AS (
    SELECT * FROM {{ ref('stg_raw__openaqs') }}
),

group_openaqs AS (
    SELECT
        raw_source_name
    FROM raw_openaqs
    GROUP BY raw_source_name
)

SELECT * FROM group_openaqs