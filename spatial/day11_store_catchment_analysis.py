from pyspark.sql import functions as F
from sedona.spark import SedonaContext

BASE = (
    "/mnt/c/Users/sreer/Downloads/"
    "GEOPULSE-HYPERLOCAL-RETAIL-MOBILITY-ANALYTICS/"
)

MOVEMENT_FILE = BASE + "sample_data/device_movement_day4.csv"
STORE_FILE = BASE + "sample_data/bengaluru_stores.csv"

CATCHMENT_METERS = 500

spark = (
    SedonaContext.builder()
    .appName("GeoPulse-Day11-Store-Catchment-Analysis")
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

    movement.createOrReplaceTempView("movement")

    print("\n===== STEP 2: CREATE MOVEMENT POINTS =====")

    points = sedona.sql("""
        SELECT
            *,
            ST_Point(
                CAST(longitude AS DOUBLE),
                CAST(latitude AS DOUBLE)
            ) AS point_geom
        FROM movement
        WHERE longitude IS NOT NULL
          AND latitude IS NOT NULL
    """)

    points.cache()
    point_count = points.count()

    print("Movement point geometries:", point_count)

    points.createOrReplaceTempView("movement_points")

    print("\n===== STEP 3: LOAD STORE LOCATIONS =====")

    stores = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(STORE_FILE)
    )

    store_count = stores.count()

    print("Total store locations:", store_count)

    stores.createOrReplaceTempView("stores")

    store_geometries = sedona.sql("""
        SELECT
            store_id,
            store_type,
            zone_id,
            longitude,
            latitude,
            ST_Point(
                CAST(longitude AS DOUBLE),
                CAST(latitude AS DOUBLE)
            ) AS store_geom
        FROM stores
    """)

    store_geometries.createOrReplaceTempView("store_points")

    print("\n===== STEP 4: CALCULATE 500-METRE CATCHMENTS =====")

    catchment_matches = sedona.sql("""
        SELECT
            s.store_id,
            s.store_type,
            s.zone_id,
            p.device_id,
            p.activity,
            ST_DistanceSphere(
                s.store_geom,
                p.point_geom
            ) AS distance_meters
        FROM store_points s
        INNER JOIN movement_points p
            ON ST_DistanceSphere(
                s.store_geom,
                p.point_geom
            ) <= 500
    """)

    catchment_matches.cache()

    match_count = catchment_matches.count()

    print("Movement points within catchments:", match_count)

    print("\n===== STEP 5: STORE CATCHMENT SUMMARY =====")

    summary = catchment_matches.groupBy(
        "store_id", "store_type", "zone_id"
    ).agg(
        F.count("*").alias("movement_point_count"),
        F.count("device_id").alias("device_ping_count"),
        F.countDistinct("device_id").alias("unique_devices"),
        F.countDistinct("activity").alias("activity_categories")
    ).orderBy("store_type", "store_id")

    summary.show(20, truncate=False)

    print("\n===== STEP 6: EXISTING VS CANDIDATE COMPARISON =====")

    summary.groupBy("store_type").agg(
        F.sum("movement_point_count").alias("total_movement_points"),
        F.sum("unique_devices").alias(
            "sum_of_store_unique_device_counts"
        )
    ).show(truncate=False)

    print("\n===== STEP 7: VALIDATION =====")

    existing_count = stores.filter(
        F.col("store_type") == "existing"
    ).count()

    candidate_count = stores.filter(
        F.col("store_type") == "candidate"
    ).count()

    print("Movement records:", movement_count)
    print("Valid point geometries:", point_count)
    print("Store locations:", store_count)
    print("Existing stores:", existing_count)
    print("Candidate stores:", candidate_count)
    print("Catchment matches:", match_count)
    print("Catchment radius:", CATCHMENT_METERS, "metres")

    if movement_count != 336000:
        raise RuntimeError("Unexpected movement record count.")

    if point_count != movement_count:
        raise RuntimeError("Some movement points are missing.")

    if store_count != 16:
        raise RuntimeError("Expected 16 store locations.")

    if existing_count != 12 or candidate_count != 4:
        raise RuntimeError("Unexpected store type counts.")

    if match_count == 0:
        raise RuntimeError("No catchment matches found.")

    print("\nGEOPULSE DAY 11 STORE CATCHMENT ANALYSIS PASSED")

finally:
    spark.stop()
    print("\nSpark session stopped.")