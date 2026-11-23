# GeoPulse â€” Development Log

## Day 1 â€” 10 November 2026

### Completed Tasks
- Created the GeoPulse GitHub repository.
- Cloned the repository to the local computer.
- Opened the project in VS Code.
- Created the initial project folder structure.
- Added README.md.
- Added .gitignore.
- Created docs/work_plan.md.

### Project Structure
Created folders:
- simulator
- warehouse
- spatial
- dbt_project
- airflow
- api
- web
- evaluation
- tests
- sample_data
- data
- docs

### Technologies Planned
Python, Snowflake, Apache Spark, Apache Sedona, dbt, Apache Airflow, FastAPI, React and Kepler.gl.

### Notes
All mobility data will be simulated. No real individual location data will be used.

### Status
Day 1 setup tasks completed.
## Day 2 - November 11, 2026: Development Environment Setup

### Completed
- Created and activated the Python virtual environment (.venv).
- Verified Python 3.14.7.
- Installed and verified NumPy 2.5.4.
- Installed and verified pandas 3.1.1.
- Installed and verified PyArrow 26.0.1.
- Installed and verified pytest 9.2.0.
- Verified pip dependencies using pip check; no broken requirements found.
- Installed and verified Node.js 24.22.2 and npm 11.19.1.
- Installed and verified Eclipse Temurin Java 11.0.33 and javac.
- Verified Git 2.55.0.

### Verification
- All required Python libraries imported successfully.
- Python virtual environment executable verified.
- Node.js, npm, Java, javac and Git commands executed successfully.
- Git working tree clean before Day 2 documentation.

### Notes
- Python 3.14.7 is being used for the initial development environment.
- Compatibility with later Spark, Sedona and other project dependencies will be tested when those components are introduced.

### Status
Environment setup and initial verification completed successfully.

## Day 3 - November 12, 2026: Bengaluru City Geography

### Completed
- Defined an approximate 10 km x 10 km simulated Bengaluru study area.
- Created a 5 x 5 grid containing 25 geographic zones.
- Classified zones into 9 residential, 9 office and 7 retail zones.
- Generated 12 existing simulated coffee-store locations.
- Generated 4 simulated candidate store locations.
- Created sample_data/bengaluru_zones.geojson.
- Created sample_data/bengaluru_stores.csv.
- Created simulator/create_city.py to reproduce the geography data.
- Added automated tests in tests/test_city_geography.py.

### Verification
- GeoJSON FeatureCollection and polygon boundaries validated.
- 25 unique zone IDs verified.
- Store CSV columns and unique store IDs verified.
- 12 existing and 4 candidate stores verified.
- Store coordinates and zone references validated.
- Five automated geography tests added.

### Notes
- Coordinates are simulated around an approximate Bengaluru reference point.
- These are not verified real-world store locations or administrative boundaries.
- No real individual location data is used.

### Status
Bengaluru simulated geography generation and validation completed.

## Day 4 - Synthetic Device Movement Simulator
- Created simulator/generate_movement.py.
- Generated synthetic movement data for 1,000 devices across 7 days.
- Produced 336,000 movement records.
- Added morning commute, working, lunch, evening, weekend and residential activities.
- Used reproducible random seed and hashed device identifiers.
- Added GPS coordinate noise.
- Validation passed: 0 missing values and 0 duplicate rows.
- Output: sample_data/device_movement_day4.csv.

## Day 5 - November 14, 2026: Parquet Conversion and Automated Testing

- Created `simulator/convert_to_parquet.py` to convert movement CSV data into Parquet format.
- Generated `sample_data/device_movement_day5.parquet`.
- Verified 336,000 records and 1,000 unique devices.
- Confirmed zero missing values and duplicate records.
- Reduced dataset size from approximately 33.13 MiB to 5.58 MiB.
- Created `tests/test_movement_data.py` with 9 automated validation tests.
- Test result: 9 passed in 3.13 seconds.
- Confirmed Parquet files are excluded from Git through `.gitignore`.


## Day 6 - November 15, 2026: Snowflake Data Warehouse Setup

- Created and configured the Snowflake trial account.
- Created database: GEOPULSE_DB.
- Created RAW schema.
- Created X-Small warehouse: GEOPULSE_WH.
- Configured auto-suspend after 60 seconds.
- Enabled automatic warehouse resume.
- Verified the active database, schema, warehouse and role.
- Saved setup SQL in warehouse/setup_snowflake.sql.

### Status
Snowflake account and initial data warehouse setup completed and verified.

## Day 7 - November 16, 2026: Snowflake Data Loading and Validation

- Loaded synthetic movement data into Snowflake.
- Target table: GEOPULSE_DB.RAW.RAW_DEVICE_MOVEMENT.
- Source file: device_movement_day4.csv.
- Successfully loaded 336,000 records.
- Verified 1,000 unique simulated devices.
- Confirmed zero null timestamps.
- Confirmed zero null device IDs.
- Confirmed zero exact duplicate records.
- Verified all seven expected activity categories.
- Created SQL validation queries in warehouse/day7_validate_movement.sql.

### Status
Snowflake movement data loading and validation completed.
## Day 8 - Spark and Sedona Setup
- Installed Python 3.10.11 in a separate `.venv-spark` environment.
- Installed PySpark 3.5.9 and Apache Sedona 1.9.1.
- Verified Java 11.0.33 and successful package imports.
- Successfully ran a local Spark calculation: 10 rows counted.
- Added automated setup tests and Day 8 documentation.
- Sedona spatial query remains pending due to the Windows Hadoop configuration limitation.

## Day 9 – Spark and Sedona Spatial Processing

**Completed:**
- Set up Ubuntu 26.04 through WSL2.
- Installed Python 3.10.22 and Java 17.
- Created dedicated `.venv-spark-ws1` environment.
- Installed PySpark 3.5.9 and Apache Sedona 1.9.1.
- Verified package compatibility using `uv pip check`.
- Downloaded the Sedona Spark 3.5 Java dependency.
- Executed a Sedona spatial SQL query successfully.

**Validation:**
- Bengaluru point: `POINT (77.5946 12.9716)`
- Result: `SEDONA SPATIAL TEST PASSED`

**Outcome:** Spark and Sedona spatial processing successfully verified in WSL2.

## Day 10 – Spark and Sedona Spatial Processing

**Completed:**
- Loaded 336,000 synthetic device movement records.
- Converted movement coordinates into Spark point geometries.
- Loaded 25 Bengaluru zone polygons.
- Performed a spatial join using Sedona ST_Contains.
- Aggregated movement records by zone and zone type.

**Validation:**
- Movement records: 336,000
- Point geometries: 336,000
- Zone polygons: 25
- Matched records: 336,000
- Unmatched records: 0

**Outcome:** GeoPulse Day 10 spatial processing successfully completed and verified using PySpark, Apache Sedona, and Shapely.

## Day 11 — Store Catchment Analysis

**Completed:**
- Loaded 336,000 synthetic movement records.
- Created 336,000 spatial point geometries using Apache Sedona.
- Loaded 12 existing stores and 4 candidate stores.
- Calculated 500-metre store catchments using `ST_DistanceSphere`.
- Identified 54,458 movement-point matches.
- Compared existing and candidate store catchment activity.
- Validated all expected record and store counts.

**Results:**
- Existing store catchment matches: 41,267.
- Candidate store catchment matches: 13,191.
- Total catchment matches: 54,458.

**Validation:** GEOPULSE DAY 11 STORE CATCHMENT ANALYSIS PASSED.

**Status:** Completed.
## Day 13 — Spatial Audit and Mid-Project Preparation

- Reran Day 10 spatial processing successfully.
- Verified 336,000 movement records and point geometries.
- Verified 25 zone polygons, 336,000 spatial matches and zero unmatched points.
- Reran Day 11 store catchment analysis successfully.
- Verified 16 stores: 12 existing and 4 candidate.
- Verified 54,458 catchment matches within 500 metres.
- Created docs/DAY13_SPATIAL_AUDIT.md.
- Confirmed all mobility data is synthetic.
- Snowflake execution of dbt models remains pending authentication.


## Day 14 — dbt Configuration and Validation

- Verified dbt Core 1.12.7 and Snowflake adapter 1.12.1.
- Successfully parsed the dbt project.
- Discovered 2 analytics models, 5 data tests and 1 source.
- Confirmed dbt profile and project configuration are valid.
- Attempted Snowflake connectivity using dbt debug.
- Connection blocked by Snowflake SAML Identity Provider error 390190.
- Model execution and dbt test execution remain unverified.
- Created docs/DAY14_DBT_VALIDATION.md.

**Status:** dbt configuration and discovery verified; Snowflake execution pending authentication.


