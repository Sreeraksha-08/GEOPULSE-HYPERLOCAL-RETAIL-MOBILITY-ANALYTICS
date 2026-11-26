# Day 17 — dbt Data Quality and Integrity Refinement

## Objective
Strengthen analytics model integrity through additional singular
SQL data-quality tests and project validation.

## Models
- mart_hourly_footfall
- mart_morning_evening_footfall

## New Tests
1. assert_unique_morning_evening_grain
   - Detects duplicate visit_date and daypart combinations.
2. assert_positive_morning_evening_footfall
   - Detects zero or negative comparison footfall values.

## Validation Evidence
- dbt Core 1.12.7.
- Snowflake adapter 1.12.1.
- dbt parse completed successfully.
- 2 models discovered.
- 1 source discovered.
- 11 data tests discovered.

## Runtime Limitation
An attempt to execute dbt test was made.
Snowflake connection failed with error 390190 (08001),
related to the SAML Identity Provider account parameter.

Individual test execution results could not be obtained.
Passing warehouse tests are not claimed.

## Outcome
Additional SQL integrity tests were created and discovered.
Project parsing and test discovery were verified.
Warehouse runtime validation remains pending authentication.
