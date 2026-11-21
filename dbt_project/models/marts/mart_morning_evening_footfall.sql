{{ config(materialized='view') }}

SELECT
    visit_date,
    daypart,
    SUM(unique_visitors) AS summed_hourly_unique_visitors
FROM {{ ref('mart_hourly_footfall') }}
WHERE daypart IN ('morning', 'evening')
GROUP BY visit_date, daypart
