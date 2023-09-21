#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

from pyspark.sql import SparkSession, SQLContext


def spark_init():
    _spark = (
        SparkSession.builder.appName("spark_env")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .master("local[*]")
        .getOrCreate()
    )

    sc = _spark.sparkContext
    _sqlContext = SQLContext(sc)

    return _spark, _sqlContext


(
    spark,
    sqlContext,
) = spark_init()
spark.sparkContext.setLogLevel("ERROR")
