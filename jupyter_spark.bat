@echo copying local.yaml in .venv/Lib/local.yaml
@echo off
copy local.yaml ".venv/Lib/local.yaml"
set PYSPARK_DRIVER_PYTHON=.\.venv\Scripts\jupyter-notebook.exe
call pyspark --packages io.delta:delta-core_2.12:1.2.1 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
pause
