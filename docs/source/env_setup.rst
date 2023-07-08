Environment setup
=================

.. _dev setup:

Initial Setup via Pycharm
--------------------------

Create a new project cloning the repository. Add new local interpreter specifying :code:`.venv` as directory
for the environment. Mark directory :code:`src` as Sources Root.

Remove references to boilerplate
--------------------------------
In pycharm hit ctrl+shift+F and search for 'boilerplate'. Replace all occurrences with your project name.


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
In this file, you can store secrets and overwrite any values to your needs without affecting anyone
else's configuration. To create it, you can run

.. code-block::

    python -m boilerplate init

The file will be located in the root folder and named :code:`local.yaml`. Fill in any value here.
To access configuration programmatically, use the :code:`get_config()` from the module
:code:`boilerplate.config`.

Database installation [Optional]
--------------------------------

Boilerplate provides Postgres database support via docker. In order to provision the database go
to folder :code:`docker` and run

.. code-block:: bash

    docker compose up

Datbase credentials can be defined in :code:`local.yaml` and accessed by

.. code-block:: python

    from boilerplate.config import conf

    username = conf.sql_login.username


Spark installation [Optional]
-----------------------------

Repository comes with spark support. Following instructions assume installation is done at path :code:`/opt`. Download spark release from
`https://spark.apache.org/downloads.html <https://spark.apache.org/downloads.html>`_ and unpack. Set environment
variable SPARK_HOME with:

.. code-block:: bash

    export SPARK_HOME=/opt/spark-3.4.1-bin-hadoop3

Set variable SPARK_LOCAL_DIRS for path were temporary files (e.g. due to memory spill) are saved.
If path does not exist, crate it.

.. code-block:: bash

    export SPARK_LOCAL_DIRS=/opt/spark_scratch

Download :code:`postgresql-42.5.4.jar` file for postgres support in spark from
`https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.4/postgresql-42.5.4.jar <https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.4/postgresql-42.5.4.jar>`_
and save it into :code:`/opt/spark-3.4.1-bin-hadoop3/jars`


If setting environment on a windows machine, download :code:`winutils.exe` for
hadoop-3.3.5 from `https://github.com/huskyui/winutils/blob/master/hadoop-3.3.5/bin/winutils.exe <https://github.com/huskyui/winutils/blob/master/hadoop-3.3.5/bin/winutils.exe>`_
and save it into :code:`C:\\spark\\hadoop-3.3.5\\bin`. Then set variable HADOOP_HOME to :code:`C:\\spark\\hadoop-3.3.5`
