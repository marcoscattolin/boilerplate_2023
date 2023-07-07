# ============================================================
# COPYRIGHT
# ============================================================
__copyright__ = "Copyright (C) 2022, Boston Consulting Group"
__license__ = "Proprietary"
__author__ = (
    "Marco Scattolin <scattolin.marco@bcg.com>",
)
# ============================================================
from boilerplate.utils.logging import logger
from boilerplate.config.config import conf

logger.info("Helloworld")
logger.info(conf.sql_login.username)

