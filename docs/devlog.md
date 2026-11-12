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
## Day 2 — November 11, 2026: Development Environment Setup

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

## Day 3 — November 12, 2026: Bengaluru City Geography

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
