from pyspark.sql import SparkSession
from sedona.spark import SedonaContext

spark = (
    SedonaContext.builder()
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
    .getOrCreate()
)

try:
    sedona = SedonaContext.create(spark)

    result = sedona.sql("""
        SELECT ST_AsText(ST_Point(77.5946, 12.9716)) AS geometry
    """)

    result.show(truncate=False)
    print("SEDONA SPATIAL TEST PASSED")

finally:
    spark.stop()
