Environment setup
=================

.. _dev setup:

Development Setup
-----------------

To install the requirements and package, fist setup a Virtual Environment using Python.
The :code:`flit` command will install all extra dependencies to run test and pre-commit hooks.
In a production scenario, you can omit the extra dependencies.

.. code-block:: bash

    $ python3.8 -m venv .venv

    $ source .venv/bin/activate

    $ pip install --upgrade pip flit wheel setuptools

    $ flit install -s --deps production --extras testing,docs,local_development

Next, install the pre-commit hooks using

.. code-block:: bash

    $ pre-commit install --install-hooks

You can verify the installation by running the test suite


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
:code:`rms.config`.

Using configuration for testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For testing, you likely want / should use different values for e.g. database connections.
The folder :code:`test/test_rms/resources` includes a file to store values specific for testing (:code:`local.testing.yaml`).
To make sure the :code:`get_config` function reads the YAML file for testing, we use
an environment variable called :code:`XCONFIG_LOCAL_YAML`. We are using a fixture
to set this before any test runs

.. code-block:: python

    @pytest.fixture(autouse=True)  # runs for any test
    def setup_config():
        os.environ["XCONFIG_LOCAL_YAML"] = os.path.join(P_RESOURCES, "local.test.yaml")



