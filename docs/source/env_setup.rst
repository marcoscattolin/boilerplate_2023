Environment setup
=================

.. _dev setup:

Initial Setup via Pycharm
--------------------------

Create new project cloning the repository. Add new local interpreter specifying :code:`.venv` as directory
for the environment. Mark directory :code:`src` as Soruces root

Packages and pre-commit installation
---------------------------------------------

To install the requirements and package the :code:`flit` command will install all extra dependencies to run test
and pre-commit hooks. In a production scenario, you can omit the extra dependencies.

.. code-block:: bash

    $ pip install --upgrade pip flit wheel setuptools

    $ flit install -s --deps production --extras testing,docs,local_development

Next, install the pre-commit hooks using

.. code-block:: bash

    $ pre-commit install --install-hooks

You can verify the installation by running the test suite

[Optional] Spark support
------------------------


[Optional] Database support
---------------------------

Boilerplate provides Postgres database support via docker. In order to provision the database go
to folder :code:`docker` and run

.. code-block:: bash

    $ docker compose up


Configuration Management
------------------------

The repository uses a Pydantic-based approach facilitated by XConfig, a library developed by BCG
internally. When cloning your first instance of the repo, you will get a lot of defaults values
already attached to the Pydantic models. Some values are not set (especially secrets).
The recommended way to store the missing values is via a YAML file not versioned by git.
In this file, you can store secrets and overwrite any values to your needs without affecting anyone
else's configuration. To create it, you can run

.. code-block::

    $ python -m boilerplate init

The file will be located in the root folder and named :code:`local.yaml`. Fill in any value here.
To access configuration programmatically, use the :code:`get_config()` from the module
:code:`boilerplate.config`.
