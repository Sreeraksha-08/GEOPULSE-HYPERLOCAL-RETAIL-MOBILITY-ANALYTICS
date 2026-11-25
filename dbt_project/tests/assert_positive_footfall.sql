SELECT
    hour_start,
    unique_visitors
FROM {{ ref('mart_hourly_footfall') }}
WHERE unique_visitors <= 0
