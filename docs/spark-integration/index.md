# Spark Integration

As of [this commit]({{ uc.commit }}/8fb49245e2aa2126901f7f69016f6762b083b238), Unity Catalog supports Apache Spark {{ spark.version }} and Delta Lake {{ delta.version }} using [UCSingleCatalog](UCSingleCatalog.md) and [UCProxy](UCProxy.md).

The following features are supported:

* Read/write (partitioned) external parquet tables
* Read/write (partitioned) external delta tables
* Support the path table syntax of delta tables

## Demo

Download Apache Spark {{ spark.version }} from [Preview release of Spark 4.0](https://spark.apache.org/news/spark-4.0.0-preview1.html).

``` shell
build/sbt clean package publishLocal
```

!!! note
    You have to change `build.sbt` to build the Spark Integration module. A fix is coming.

``` shell
./bin/spark-shell \
  --conf spark.jars.ivy=$HOME/.ivy2 \
  --packages \
    io.delta:delta-spark_2.13:{{ delta.version }},io.unitycatalog:unitycatalog-spark:0.1.0-SNAPSHOT \
  --conf spark.sql.catalog.unity=io.unitycatalog.connectors.spark.UCSingleCatalog \
  --conf spark.sql.catalog.unity.uri=http://localhost:8080 \
  --conf spark.sql.catalog.unity.token=not_used_token
```

```text
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 4.0.0-preview1
      /_/

Using Scala version 2.13.14 (OpenJDK 64-Bit Server VM, Java 17.0.11)
Type in expressions to have them evaluated.
Type :help for more information.
Spark context Web UI available at http://192.168.68.100:4040
Spark context available as 'sc' (master = local[*], app id = local-1720981549342).
Spark session available as 'spark'.
```

```scala
assert(spark.version == "{{ spark.version }}", "Unity Catalog supports Apache Spark {{ spark.version }}")
assert(io.delta.VERSION == "{{ delta.version }}", "Unity Catalog supports Delta Lake {{ delta.version }}")
```

``` text
scala> spark.catalog.listTables
...
scala.NotImplementedError: an implementation is missing
  at scala.Predef$.$qmark$qmark$qmark(Predef.scala:344)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listTables(UCSingleCatalog.scala:37)
  at org.apache.spark.sql.execution.datasources.v2.ShowTablesExec.run(ShowTablesExec.scala:40)
  at org.apache.spark.sql.execution.datasources.v2.V2CommandExec.result$lzycompute(V2CommandExec.scala:43)
  at org.apache.spark.sql.execution.datasources.v2.V2CommandExec.result(V2CommandExec.scala:43)
  at org.apache.spark.sql.execution.datasources.v2.V2CommandExec.executeCollect(V2CommandExec.scala:49)
...
```

``` text
scala> spark.catalog.tableExists("unity.default.numbers")
org.apache.spark.sql.delta.DeltaAnalysisException: [DELTA_CONFIGURE_SPARK_SESSION_WITH_EXTENSION_AND_CATALOG] This Delta operation requires the SparkSession to be configured with the
DeltaSparkSessionExtension and the DeltaCatalog. Please set the necessary
configurations when creating the SparkSession as shown below.

  SparkSession.builder()
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    ...
    .getOrCreate()

If you are using spark-shell/pyspark/spark-submit, you can add the required configurations to the command as show below:
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog

  at org.apache.spark.sql.delta.DeltaErrorsBase.configureSparkSessionWithExtensionAndCatalog(DeltaErrors.scala:1698)
  at org.apache.spark.sql.delta.DeltaErrorsBase.configureSparkSessionWithExtensionAndCatalog$(DeltaErrors.scala:1695)
  at org.apache.spark.sql.delta.DeltaErrors$.configureSparkSessionWithExtensionAndCatalog(DeltaErrors.scala:3413)
  at org.apache.spark.sql.delta.DeltaLog.checkRequiredConfigurations(DeltaLog.scala:625)
  ... 133 elided
```