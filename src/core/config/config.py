#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import logging
import os
import pathlib
from typing import Optional, Union

import yaml
from pydantic import BaseModel, SecretStr

from ._xconfig import BaseConfigProvider, XConfig

base_path = pathlib.Path(__file__).parent.parent.parent.parent
if ".venv" in base_path.parts:
    base_path = base_path.parent.parent
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
    * default location -> base path variable + local.yaml (lowest priority)

    :param reload: if True, the config will be reloaded from disk even if
        it is a configuration object already exists.
        This is mainly useful in interactive environments like notebooks
    :param local_yaml: Path to a yaml file that you can use to store sensible data.
        Three sources for this value - listed in the order of priority they take (least first):
            - os.environ['XCONFIG_LOCAL_YAML'] if exists, is taken
            - default: if the file 'local.yaml' if exists, is taken
            - local_yaml function argument if provided, is taken
    :param env_prefix: Optional value to prefix environment variables.
        E.g. you can use 'DEV_' as the `env_prefix` and then all your config
        values are expected to start with 'DEV_', for example 'DEV_POSTGRES_DB'.
        If you want to exclude certain variables from the prefixing you can use field(..., env='fixed_name')
        to set the value in the config class for this value.
    """
    if local_yaml is None:
        local_yaml = os.environ.get("XCONFIG_LOCAL_YAML", None)
    if local_yaml is None and os.path.isdir(os.path.join(base_path, "configs")):
        local_yaml = os.path.join(base_path, "configs")
    if local_yaml is None:
        return __provider.get_config(
            reload=reload, env_prefix=env_prefix, *args, **kwargs
        )
    else:
        extra_config = dict()
        files = [os.path.join(local_yaml, f) for f in os.listdir(local_yaml)]
        for f in files:
            with open(f, "r") as stream:
                current_config = yaml.safe_load(stream)
                extra_config = {**extra_config, **current_config}
        if extra_config is None:
            extra_config = dict()
        # merge dicts, kwargs have priority
        extra_args = {**extra_config, **kwargs}
        return __provider.get_config(
            reload=reload, env_prefix=env_prefix, *args, **extra_args
        )


conf = get_config()
