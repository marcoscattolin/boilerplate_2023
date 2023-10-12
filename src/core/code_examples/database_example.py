#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import pandas as pd
from sqlalchemy import create_engine

from core.config.config import conf
from core.utils.logging import logger

# read from file
df = pd.read_csv("../../../data/test.csv.dummy", parse_dates=True)
df["COLUMN_C"] = pd.to_datetime(df["COLUMN_C"])


# establish connections
conn_string = (
    f"postgresql://{conf.sql_login.username}:{conf.sql_login.password.get_secret_value()}"
    f"@{conf.sql_connection.server}/{conf.sql_connection.db_name}"
)
engine = create_engine(conn_string)

# write to database
df.to_sql("POSTGRES_TABLE", con=engine, if_exists="replace", index=False)
logger.info(f"Saved {df.shape[0]} rows.")


# read from database
loaded_df = pd.read_sql("POSTGRES_TABLE", con=engine)
logger.info(f"Loaded {loaded_df.shape[0]} rows.")

engine.dispose()
