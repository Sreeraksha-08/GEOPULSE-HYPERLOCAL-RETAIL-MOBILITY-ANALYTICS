import json

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType
)
from sedona.spark import SedonaContext
from shapely.geometry import shape

BASE = (
    "/mnt/c/Users/sreer/Downloads/"
    "GEOPULSE-HYPERLOCAL-RETAIL-MOBILITY-ANALYTICS/"
)

MOVEMENT_FILE = BASE + "sample_data/device_movement_day4.csv"
ZONE_FILE = BASE + "sample_data/bengaluru_zones.geojson"

spark = (
    SedonaContext.builder()
    .appName("GeoPulse-Day10-Spatial-Processing")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.9.1"
    )
    .config(
        "spark.serializer",
        "org.apache.spark.serializer.KryoSerializer"
    )
    .config(
        "spark.kryo.registrator",
        "org.apache.sedona.core.serde.SedonaKryoRegistrator"
    )
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

try:
    sedona = SedonaContext.create(spark)

    print("\n===== STEP 1: LOAD MOVEMENT DATA =====")

    movement = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(MOVEMENT_FILE)
    )

    movement_count = movement.count()
    print("Movement records:", movement_count)

    print("\n===== STEP 2: CREATE POINT GEOMETRIES =====")

    movement.createOrReplaceTempView("movement")

    points = sedona.sql("""
        SELECT *,
               ST_Point(
                   CAST(longitude AS DOUBLE),
                   CAST(latitude AS DOUBLE)
               ) AS point_geom
        FROM movement
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
    """)

    points.createOrReplaceTempView("movement_points")

    point_count = points.count()
    print("Point geometries:", point_count)

    points.select(
        "device_id", "latitude", "longitude", "point_geom"
    ).show(5, truncate=False)

    print("\n===== STEP 3: READ GEOJSON POLYGONS =====")

    with open(ZONE_FILE, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    zone_rows = []

    for feature in geojson["features"]:
        properties = feature["properties"]
        polygon = shape(feature["geometry"])

        zone_rows.append((
            str(properties["zone_id"]),
            str(properties["zone_type"]),
            polygon.wkt
        ))

    zone_schema = StructType([
        StructField("zone_id", StringType(), False),
        StructField("zone_type", StringType(), False),
        StructField("geometry_wkt", StringType(), False)
    ])

    zone_data = spark.createDataFrame(
        zone_rows, schema=zone_schema
    )

    zone_data.createOrReplaceTempView("zone_data")

    zones = sedona.sql("""
        SELECT
            zone_id,
            zone_type,
            ST_GeomFromWKT(geometry_wkt) AS geometry
        FROM zone_data
    """)

    zones.createOrReplaceTempView("zones")

    zone_count = zones.count()

    print("Zone polygons loaded:", zone_count)
    zones.select(
        "zone_id", "zone_type", "geometry"
    ).show(3, truncate=False)

    print("\n===== STEP 4: SPATIAL JOIN =====")

    joined = sedona.sql("""
        SELECT
            p.device_id,
            p.timestamp,
            p.activity,
            p.zone_id AS recorded_zone,
            z.zone_id AS matched_zone,
            z.zone_type,
            p.point_geom
        FROM movement_points p
        JOIN zones z
          ON ST_Contains(z.geometry, p.point_geom)
    """)

    joined.cache()

    matched_count = joined.count()

    print("Spatially matched records:", matched_count)

    print("\n===== STEP 5: ZONE ACTIVITY SUMMARY =====")

    joined.groupBy(
        "matched_zone", "zone_type"
    ).count().orderBy(
        "matched_zone"
    ).show(30, truncate=False)

    print("\n===== STEP 6: VALIDATION =====")

    unmatched_count = point_count - matched_count

    print("Movement points:", point_count)
    print("Matched points:", matched_count)
    print("Unmatched points:", unmatched_count)
    print("Zone polygons:", zone_count)

    if zone_count != 25:
        raise RuntimeError("Expected exactly 25 zone polygons.")

    if matched_count > 0:
        print("\nGEOPULSE DAY 10 SPATIAL PROCESSING PASSED")
    else:
        raise RuntimeError("No spatial matches found.")

finally:
    spark.stop()
    print("\nSpark session stopped.")