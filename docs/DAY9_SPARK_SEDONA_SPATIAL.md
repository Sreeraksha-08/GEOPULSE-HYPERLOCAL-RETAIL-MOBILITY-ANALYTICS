# Day 9 – Spark and Sedona Spatial Processing

## Objective
Set up Apache Spark and Apache Sedona in Ubuntu through WSL2 and verify spatial SQL functionality.

## Environment
- Operating System: Ubuntu 26.04.1 LTS (WSL2)
- Python: 3.10.22
- Java: OpenJDK 17.0.21
- PySpark: 3.5.9
- Apache Sedona: 1.9.1
- Pandas: 2.2.3
- NumPy: 2.2.6
- Pytest: 9.2.0

## Setup
Created a dedicated Python virtual environment named `.venv-spark-ws1`.

Installed PySpark, Apache Sedona and supporting Python packages.

Configured Spark with:
- Sedona shaded JAR for Spark 3.5 and Scala 2.12
- KryoSerializer
- SedonaKryoRegistrator

## Spatial SQL Verification

Executed the following spatial SQL query:

```sql
SELECT ST_AsText(ST_Point(77.5946, 12.9716)) AS geometry;
```

Verified output:

```text
POINT (77.5946 12.9716)
```

**Result: SEDONA SPATIAL TEST PASSED**

## Issues Resolved
The Windows Spark environment encountered a Hadoop `winutils.exe` configuration issue.

Moved spatial test execution to Ubuntu through WSL2, avoiding the Windows Hadoop dependency issue.

## Warnings and Limitations
- Native Hadoop library warning appeared during execution.
- GeoTools was not available on the classpath.
- The tested vector point-geometry operation completed successfully.
- Raster operations were not verified.

## Day 9 Outcome
- Python and Java environments verified.
- PySpark and Sedona imports successful.
- Sedona Java dependency downloaded successfully.
- Spark spatial SQL query executed successfully.
- Bengaluru point geometry verified.

**Status: Spatial test completed successfully.**