#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

import os
import pathlib
import shutil

import click
import cowsay

base_path = pathlib.Path(__file__).parent.parent.parent
if ".venv" in base_path.parts:
    base_path = base_path.parent.parent


def initialize_local_default_config() -> pathlib.Path:
    """
    This function should be called once when starting to work on the repo.
    Copies the template file into the base directory.

    Returns: Copy destination
    """
    src = pathlib.Path(__file__).parent / "config" / ".local.template.yaml"
    dst = base_path / "local.yaml"
    if os.path.isfile(dst):
        raise FileExistsError(dst)
    shutil.copy(src=src, dst=dst)
    return dst


@click.group()
def cli():
    """
    Initialize cli
    """


@click.command(name="init")
def init():
    output_path = initialize_local_default_config()
    cowsay.cow(
        "Initialized Config 🥳. You can find a template of the config file in "
        f"`{output_path}` in the project root dir."
    )


cli.add_command(init)
# noinspection PyTypeChecker

if __name__ == "__main__":
    cli()
