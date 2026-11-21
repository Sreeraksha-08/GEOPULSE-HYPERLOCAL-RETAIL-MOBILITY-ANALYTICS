{{ config(materialized='table') }}

WITH retail_visits AS (
    SELECT
        "TIMESTAMP" AS event_timestamp,
        DEVICE_ID
    FROM {{ source('raw', 'raw_device_movement') }}
    WHERE LOWER(ZONE_TYPE) = 'retail'
      AND LOWER(ACTIVITY) IN (
          'lunch_visit',
          'evening_visit',
          'weekend_visit'
      )
      AND "TIMESTAMP" IS NOT NULL
      AND DEVICE_ID IS NOT NULL
),

hourly AS (
    SELECT
        DATE_TRUNC('HOUR', event_timestamp) AS hour_start,
        COUNT(DISTINCT DEVICE_ID) AS unique_visitors
    FROM retail_visits
    GROUP BY DATE_TRUNC('HOUR', event_timestamp)
)

SELECT
    hour_start,
    CAST(hour_start AS DATE) AS visit_date,
    EXTRACT(HOUR FROM hour_start) AS visit_hour,
    CASE
        WHEN EXTRACT(HOUR FROM hour_start) BETWEEN 6 AND 11
            THEN 'morning'
        WHEN EXTRACT(HOUR FROM hour_start) BETWEEN 12 AND 16
            THEN 'afternoon'
        WHEN EXTRACT(HOUR FROM hour_start) BETWEEN 17 AND 21
            THEN 'evening'
        ELSE 'overnight'
    END AS daypart,
    unique_visitors
FROM hourly
