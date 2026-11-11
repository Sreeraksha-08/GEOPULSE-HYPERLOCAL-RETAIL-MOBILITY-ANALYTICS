# GeoPulse — Development Log

## Day 1 — 10 November 2026

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
## Day 2 � November 11, 2026: Development Environment Setup

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
