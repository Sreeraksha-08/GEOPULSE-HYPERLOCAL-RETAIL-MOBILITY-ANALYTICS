SELECT
    visit_date,
    daypart,
    COUNT(*) AS duplicate_count
FROM {{ ref('mart_morning_evening_footfall') }}
GROUP BY visit_date, daypart
HAVING COUNT(*) > 1
