# Day 14 — dbt Configuration and Validation

## Objective
Validate the GeoPulse dbt project, discover analytics models and check
connectivity to Snowflake.

## Environment
- Python: 3.10.22
- dbt Core: 1.12.7
- dbt-snowflake: 1.12.1
- Operating environment: WSL2 Ubuntu

## Verified Results

### dbt Project Parsing
- `dbt parse --project-dir dbt_project --no-partial-parse`
- Result: Passed.

### Model Discovery
- `dbt ls --project-dir dbt_project --resource-type model`
- Result: Passed.
- Models discovered: 2.
  - `mart_hourly_footfall`
  - `mart_morning_evening_footfall`
- Data tests discovered: 5.
- Sources discovered: 1.
- Macros discovered: 563.

### Profile Configuration
- profiles.yml found and valid.
- dbt_project.yml found and valid.
- Git dependency check passed.
- Snowflake profile settings were successfully read.

### Snowflake Connectivity
- Command: `dbt debug --project-dir dbt_project`
- Result: Connection failed.
- Error: `390190 (08001)`
- Reported issue: SAML Identity Provider account parameter.
- Authentication method: externalbrowser.

## Limitations
Snowflake authentication prevented a live database connection.
Consequently, model execution, warehouse-side validation and dbt test
execution are not confirmed by this day's checks.

## Day 14 Status
dbt parsing, configuration and model discovery verified.
Snowflake connectivity remains blocked by the SAML authentication issue.
No successful model execution is claimed.
