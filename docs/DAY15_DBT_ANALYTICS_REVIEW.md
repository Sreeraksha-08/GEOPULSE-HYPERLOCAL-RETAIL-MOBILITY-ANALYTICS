# Day 15 — dbt Analytics Model Review

## Objective
Review and validate the existing GeoPulse dbt analytics models,
source configuration and schema tests.

## Models Reviewed

### 1. mart_hourly_footfall
- Materialization: table
- Source: GEOPULSE_DB.RAW.RAW_DEVICE_MOVEMENT
- Filters retail-zone visits.
- Includes lunch_visit, evening_visit and weekend_visit activities.
- Excludes null timestamps and device IDs.
- Aggregates distinct synthetic devices by hour.
- Derives visit date, hour and daypart.

### 2. mart_morning_evening_footfall
- Materialization: view
- References mart_hourly_footfall.
- Filters morning and evening dayparts.
- Aggregates hourly distinct-device counts by date and daypart.

Note: The summed hourly distinct-device count is not equivalent
to the number of distinct devices across an entire day.

## Configuration Review
- Source YAML reviewed.
- Model schema YAML reviewed.
- Source database and schema reference the existing Snowflake
  raw table.
- Five data tests are configured:
  - not_null: hour_start
  - unique: hour_start
  - not_null: unique_visitors
  - not_null: visit_date
  - not_null: daypart

## Validation Evidence
- dbt Core: 1.12.7
- dbt Snowflake adapter: 1.12.1
- dbt parse: PASSED
- Model discovery: 2 models found
- Data-test discovery: 5 tests found
- Source discovery: 1 source found
- Macros discovered: 563
- Manual SQL and YAML review: COMPLETED
- Compiled SQL artifacts: Not generated
- Snowflake connection: Blocked by SAML Identity Provider
  authentication error 390190 (08001).

## Limitations
The Snowflake authentication issue prevented successful
warehouse-dependent compilation and execution.

No claim is made that either model has been materialized
or that the five data tests have passed at runtime.

## Day 15 Outcome
The existing dbt models and configuration have been reviewed.
Project parsing and resource discovery are verified.
Warehouse execution and runtime testing remain pending
until Snowflake authentication is restored.
