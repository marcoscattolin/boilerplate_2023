Folder Tree Structure
=====================

.. _folder_tree_structure:


Source Folder
-------------

The folder :code:`src` is meant to host all the code that has to developed. Sub-folders are structured as follows:

:code:`boilerplate`: meant to host the code to be developed. Create sub-folders and insert code inside here.
:code:`boilerplate/code_examples`: contains a few example of how to use spark and database support.
:code:`boilerplate/config`: contains scripts used to load configuration parameters from yaml file.
:code:`boilerplate/utils`: contains scripts used to instantiate logger and spark session.

:code:`airflow_dags`: can be used to host airflow dags.
:code:`notebooks`: can be used to develop jupyter notebooks.


Other Folders
-------------

:code:`.venv`: virtual environment files, is created at environment setup time when a the local interpreter is created.
:code:`data`: can be used for file containing data. Extension csv, xlsx, xls, parquet are git-ignored by default.
:code:`docker`: contains the docker-compose.yml file used to start the postgres database, if needed.
:code:`docs`: contains the sphinx documentation.
:code:`logs`: logs are printed both to console and to log files saved here. File logging uses rotating logs to avoid log proliferation.
:code:`test`: can be used for test scripts.


Files in Content Root
---------------------

:code:`jupyter_spark.bat`: can be used to initialize a jupyter notebook session including a spark session.
:code:`local.yaml`: configuration parameters. To tweak and adjust, remember to update :code:`src/boilerplate/config/.local.template.yaml`
:code:`pyproject.toml`: definition of dependencies
:code:`tox.ini`: configuration of precommit hooks
:code:`.pre-commit-config.yaml`: configuration of precommit hooks
:code:`.gitignore`
:code:`README.md`
