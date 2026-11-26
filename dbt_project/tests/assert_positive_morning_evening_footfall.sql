SELECT
    visit_date,
    daypart,
    summed_hourly_unique_visitors
FROM {{ ref('mart_morning_evening_footfall') }}
WHERE summed_hourly_unique_visitors <= 0
