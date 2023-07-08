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

# read from file
df = spark.read.csv("../../../data/test.csv", header=True)

# print count
print(f"Count is: {df.count()}")

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
    .option("password", conf.sql_login.password)
    .save()
)
