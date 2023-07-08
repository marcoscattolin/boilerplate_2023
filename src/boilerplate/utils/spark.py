# ============================================================
# COPYRIGHT
# ============================================================
__copyright__ = "Copyright (C) 2022, Boston Consulting Group"
__license__ = "Proprietary"
__author__ = (
    "Marco Scattolin <scattolin.marco@bcg.com>",
)
# ============================================================
from pyspark.sql import SparkSession, SQLContext

def spark_init():
    _spark = (
        SparkSession
        .builder
        .appName("Boilerplate")
        .master("local[*]")
        .getOrCreate()
    )

    sc = _spark.sparkContext
    _sqlContext = SQLContext(sc)

    return _spark, _sqlContext


spark, sqlContext, = spark_init()
spark.sparkContext.setLogLevel("ERROR")
