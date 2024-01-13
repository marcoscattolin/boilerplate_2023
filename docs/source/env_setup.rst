Environment setup
=================

.. _dev setup:


Initial Setup via Pycharm
--------------------------

Run this steps in order

Create a new project cloning the repository. Add new local interpreter specifying :code:`.venv` as directory
for the environment. Mark directory :code:`src` as Sources Root.

.. code-block:: bash

    python -m venv .venv

and activate it

.. code-block:: bash

    .venv\Scripts\activate


Packages and pre-commit installation
---------------------------------------------

To install requirements and packages use :code:`flit`. Following commands will install all extra dependencies
and pre-commit hooks. In a production scenario, you can omit the extra dependencies.

.. code-block:: bash

    pip install --upgrade pip flit wheel setuptools

.. code-block:: bash

    flit install -s --deps production --extras testing,docs,local_development

Next, install the pre-commit hooks using

.. code-block:: bash

    pre-commit install --install-hooks

You can verify the installation by running the test suite.

Configuration Management
------------------------

The repository uses a Pydantic-based approach facilitated by XConfig, a library developed by BCG
internally. When cloning your first instance of the repo, you will get a lot of defaults values
already attached to the Pydantic models. Some values are not set (especially secrets).
The recommended way to store the missing values is via a YAML file not versioned by git.
In the yaml files, you can store secrets and overwrite any values to your needs without affecting anyone
else's configuration. To create it, you can run

.. code-block::

    python -m core init

The configuration files will be located in :code:`configs`. To access configuration programmatically, use the :code:`get_config()` from the module
:code:`core.config`.

Database installation [Optional]
--------------------------------

Postgres database support is provided via docker. In order to provision the database go
to folder :code:`docker` and run

.. code-block:: bash

    docker compose up database

Datbase credentials can be defined in :code:`local.yaml` and accessed by

.. code-block:: python

    from core.config import conf

    username = conf.sql_login.username



Dockerized Development Environment
----------------------------------

This repository includes a dockerized virtual environment to simplify execution of spark jobs from local development machines.

To build the image go to path `./docker` and run

.. code-block:: bash

    docker compose up venv

Then in pycharm, add a new remote interpreter using the docker-compose service `venv` as remote interpreter. Here below the detailed steps:

    - In Pycharm, add new interpreter "On Docker Compose"
    - Select file `docker-compose.yml` and then service `venv`
    - Keep default python interpreter `/usr/bin/python3`

Now you can run python scripts from pycharm using the dockerized interpreter.

Jupyter Notebooks from docker
-----------------------------

To run jupyter notebooks, you can use the dockerized environment. To do so launch the venv from Pycharm by:

    - opening the `docker-compose.yml` file
    - click the green play arrow in the gutter of the `venv` service
    - then access Services tab in the bottom of the IDE and click on the running `venv`
    - click the Terminal tab and execute `jupyter notebook`


Airflow DAGS Execution
----------------------

You can also run Airflow DAG's using the dockerized virtual environment. To do so launch the venv from Pycharm by:

    - opening the `docker-compose.yml` file
    - click the green play arrow in the gutter of the `venv` service
    - then access Services tab in the bottom of the IDE and click on the running `venv`
    - click the Terminal tab and execute `airflow scheduler`
    - open one more Terminal tab and execute `airflow webserver`
    - via browser, access the Airflow UI at `http://localhost:8080` (credentials are defined in `Dockerfile.venv`)
    - you can now trigger DAGs in `src/core/airflow_dags` from the UI
