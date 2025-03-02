WITH raw_openaq AS (
    SELECT * FROM {{ ref('stg_raw__openaqs') }}
),

fetch_air AS (
    SELECT
        pull_date,
        air_value,
        summary_flatten.key,
        summary_flatten.value
    FROM (
        SELECT 
            pull_date,
            "'air pollution measurement'" AS air_value,
            raw_summary
        FROM (
            SELECT 
                raw_openaq.pull_date AS pull_date,
                raw_openaq.context AS context, 
                raw_flatten.value:value AS raw_value,
                raw_flatten.value:summary AS raw_summary
            FROM 
                raw_openaq, 
                LATERAL FLATTEN(INPUT => raw_openaq.raw_data['results']) AS raw_flatten 
        ) PIVOT (
            MIN(raw_value) FOR context IN ('air pollution measurement')
        )
    ),
    LATERAL FLATTEN(INPUT => raw_summary) AS summary_flatten
)

SELECT * FROM fetch_air
