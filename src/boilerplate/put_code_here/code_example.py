# ============================================================
# COPYRIGHT
# ============================================================
__copyright__ = "Copyright (C) 2022, Boston Consulting Group"
__license__ = "Proprietary"
__author__ = (
    "Marco Scattolin <scattolin.marco@bcg.com>",
)


# ============================================================
from boilerplate.utils.spark import spark
from boilerplate.config import conf
import pyspark.sql.functions as func
from boilerplate.utils.logging import logger

# read from file
df = (
    spark.read.csv("../../../data/test.csv.dummy", header=True)
)

# convert data types
df = (
    df
    .withColumn("COLUMN_A", func.col("COLUMN_A").cast("float"))
    .withColumn("COLUMN_C", func.to_date(func.col("COLUMN_C"), format="yyyy-MM-dd"))
)

# write to database
db_url = f"jdbc:postgresql://{conf.sql_connection.server}:{conf.sql_connection.port}/{conf.sql_connection.db_name}"
(
    df
    .write
    .format("jdbc")
    .option("url", db_url)
    .option("driver", "org.postgresql.Driver")
    .option("dbtable", "POSTGRES_TABLE")
    .option("user", conf.sql_login.username)
    .option("password", conf.sql_login.password.get_secret_value())
    .mode("overwrite")
    .save()
)

logger.info(f"Saved {df.count()} rows.")
