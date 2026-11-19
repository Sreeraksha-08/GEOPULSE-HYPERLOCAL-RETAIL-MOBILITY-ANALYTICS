Day 10 – Spatial Data Processing with Apache Spark and Sedona

Objective

Perform spatial data processing on synthetic device movement records and Bengaluru zone polygons using Apache Spark and Apache Sedona.

Implementation

- Loaded 336,000 device movement records using PySpark.
- Converted latitude and longitude coordinates into spatial point geometries.
- Loaded 25 zone polygons from the GeoJSON file.
- Converted polygon geometries into Sedona spatial geometries.
- Performed a spatial join using "ST_Contains".
- Aggregated movement records by zone and zone type.

Validation Results

Validation| Result
Movement records| 336,000
Point geometries| 336,000
Zone polygons| 25
Spatially matched records| 336,000
Unmatched records| 0
Spatial processing| PASSED

Technologies

- Python
- Apache Spark (PySpark)
- Apache Sedona
- Shapely
- GeoJSON

Outcome

Successfully completed spatial point-in-polygon processing. All 336,000 movement records were matched to the 25 simulated Bengaluru zones.

Status: Day 10 completed and runtime verified.