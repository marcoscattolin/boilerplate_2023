#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

from pyspark.sql import SparkSession, SQLContext


def spark_init():
    _spark = (
        SparkSession.builder.appName("Boilerplate").master("local[*]").getOrCreate()
    )

    sc = _spark.sparkContext
    _sqlContext = SQLContext(sc)

    return _spark, _sqlContext


(
    spark,
    sqlContext,
) = spark_init()
spark.sparkContext.setLogLevel("ERROR")
