#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import pyspark.sql.functions as func

from core.config import conf
from core.utils.logging import logger
from core.utils.spark import spark

# read from file
df = spark.read.csv("../../../data/test.csv.dummy", header=True)

# convert data types
df = df.withColumn("COLUMN_A", func.col("COLUMN_A").cast("float")).withColumn(
    "COLUMN_C", func.to_date(func.col("COLUMN_C"), format="yyyy-MM-dd")
)

# write to database
db_url = f"jdbc:postgresql://{conf.sql_connection.server}:{conf.sql_connection.port}/{conf.sql_connection.db_name}"
(
    df.write.format("jdbc")
    .option("url", db_url)
    .option("driver", "org.postgresql.Driver")
    .option("dbtable", "POSTGRES_TABLE")
    .option("user", conf.sql_login.username)
    .option("password", conf.sql_login.password.get_secret_value())
    .mode("overwrite")
    .save()
)

logger.info(f"Saved {df.count()} rows.")


# read from database
loaded_df = (
    spark.read.format("jdbc")
    .option("url", db_url)
    .option("driver", "org.postgresql.Driver")
    .option("dbtable", "POSTGRES_TABLE")
    .option("user", conf.sql_login.username)
    .option("password", conf.sql_login.password.get_secret_value())
    .load()
)
logger.info(f"Loaded {loaded_df.count()} rows.")
