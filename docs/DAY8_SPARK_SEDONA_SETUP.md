# Day 8 – Spark and Sedona Environment Setup

## Completed
- Installed Python 3.10.11.
- Created a separate `.venv-spark` environment.
- Installed PySpark 3.5.9.
- Installed Apache Sedona 1.9.1.
- Installed pandas 2.2.3.
- Verified Java 11.0.33.
- Verified PySpark and Sedona imports.
- Started a local Spark session successfully.
- Verified `spark.range(10).count()` returned 10.
- Confirmed `pip check` reported no broken requirements.

## Known limitation
A Sedona spatial query has not yet passed on Windows.
Spark reported that `winutils.exe` was not found and
`HADOOP_HOME` was unset. These warnings did not prevent
the basic Spark calculation.

## Status
Spark environment setup verified.
Sedona spatial processing remains pending.
