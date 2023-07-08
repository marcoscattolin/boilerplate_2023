# ============================================================
# COPYRIGHT
# ============================================================
__copyright__ = "Copyright (C) 2022, Boston Consulting Group"
__license__ = "Proprietary"
__author__ = (
    "Marco Scattolin <scattolin.marco@bcg.com>",
)
# ============================================================
import logging
import os
import pathlib
from datetime import date
from typing import List, Optional, Union

import yaml
from airflow.models import Variable
from airflow.utils.helpers import merge_dicts
from pydantic import BaseModel, Field, PositiveInt, SecretStr

from ._xconfig import BaseConfigProvider, XConfig

base_path = pathlib.Path(__file__).parent.parent.parent.parent
logging.getLogger("airflow.models.variable").setLevel(logging.CRITICAL)


class BlobStorageLogin(BaseModel):
    """
    Pydantic data model for Azure blob storage container
    """

    account_name: str = None
    account_key: str = None


class SqlLogin(BaseModel):
    """
    Pydantic data model for sql login parameters
    """

    username: str
    password: SecretStr


class SqlConnection(BaseModel):
    """
    Pydantic data model for sql connection parameters
    """

    driver_path: str
    server: str
    port: int
    db_name: str



class Config(XConfig):

    source: str  # to check where the config it read from. Can be anything, but not 'test'

    blob_storage_login: BlobStorageLogin

    sql_login: SqlLogin

    sql_connection: SqlConnection


class __Provider(BaseConfigProvider[Config]):
    pass


__provider = __Provider()


def get_config(
    reload=False,
    local_yaml: Optional[Union[str, pathlib.Path]] = None,
    env_prefix="",
    *args,
    **kwargs,
) -> Config:
    """
    Get the configuration object.

    The function will try to read the local yaml path from different sources in this order:
    * OS environment variable (highest priority)
    * Airflow Variable
    * default location -> base path variable + local.yaml (lowest priority)

    :param reload: if True, the config will be reloaded from disk even if
        it is a configuration object already exists.
        This is mainly useful in interactive environments like notebooks
    :param local_yaml: Path to a yaml file that you can use to store sensible data.
        Three sources for this value - listed in the order of priority they take (least first):
            - default: if the file 'local.yaml' if exists, is taken
            - os.environ['XCONFIG_LOCAL_YAML'] if exists, is taken
            - local_yaml function argument if provided, is taken
    :param env_prefix: Optional value to prefix environment variables.
        E.g. you can use 'DEV_' as the `env_prefix` and then all your config
        values are expected to start with 'DEV_', for example 'DEV_POSTGRES_DB'.
        If you want to exclude certain variables from the prefixing you can use field(..., env='fixed_name')
        to set the value in the config class for this value.
    """
    if local_yaml is None:
        local_yaml = os.environ.get("XCONFIG_LOCAL_YAML", None)
    if local_yaml is None:
        local_yaml = Variable.get("XCONFIG_LOCAL_YAML", None)
    if local_yaml is None and os.path.isfile(os.path.join(base_path, "local.yaml")):
        local_yaml = os.path.join(base_path, "local.yaml")

    if local_yaml is None:
        return __provider.get_config(
            reload=reload, env_prefix=env_prefix, *args, **kwargs
        )
    else:
        with open(local_yaml, "r") as stream:
            extra_config = yaml.safe_load(stream)
        if extra_config is None:
            extra_config = dict()
        extra_args = merge_dicts(extra_config, kwargs)
        return __provider.get_config(
            reload=reload, env_prefix=env_prefix, *args, **extra_args
        )


conf = get_config()
