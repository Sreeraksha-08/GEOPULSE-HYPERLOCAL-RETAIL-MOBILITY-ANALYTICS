# GeoPulse Day 12 — Data Integrity Check

## Objective
Validate the hourly retail footfall mart against the synthetic movement data.

## Footfall definition
A visitor is a distinct device recorded in a retail zone with one of:
- lunch_visit
- evening_visit
- weekend_visit

Office, commuting, residential and return-home activities are excluded.

## Aggregation
- Grouping: event timestamp truncated to the hour.
- Metric: COUNT(DISTINCT DEVICE_ID).
- Dayparts: morning (06:00–11:59), afternoon (12:00–16:59),
  evening (17:00–21:59), overnight (other hours).
- Timestamps retain the source's recorded time; no timezone conversion
  is applied.

## Integrity checks
- Hourly key must be non-null and unique.
- Visitor count must be non-null.
- Compare hourly peaks with simulator activity windows.
- Compare morning and evening retail activity separately.
- Reconcile source and mart totals before claiming validation.

## Status
Project files created. Runtime and Snowflake reconciliation are pending
until dbt profile connectivity and model execution are verified.

## Morning-versus-evening comparison
The companion view groups the hourly mart by date and daypart.
Its metric is the sum of hourly distinct-device counts, not daily
distinct visitors. Snowflake execution and reconciliation remain pending.
