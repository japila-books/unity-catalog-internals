---
hide:
- navigation
---

# Demo: Spark Connector

This demo shows how to set up a Spark application (namely `spark-shell` and `pyspark`) with Unity Catalog using the [Spark Connector](../spark-connector/index.md) module.

## (optional) Build Spark Connector

Build the Spark Connector module.

In the directory where you cloned the Unity Catalog repo to, execute the following:

```shell
./build/sbt \
    -DsparkVersion=4.2.0 \
    -DdeltaVersion=4.4.1 \
    -DskipDeltaSpark=true \
    clean package publishLocal spark/publishLocal
```

??? warning "Apache Spark 4.3.0 Not Supported"
    [Apache Spark 4.3.0](https://spark.apache.org/news/spark-4-3-0-released.html) was released on Oct 30, 2026.
    Unity Catalog 0.7.0 builds with [Apache Spark 4.1.0]({{ uc.github }}/project/spark-versions.json#L2) by default.
    You can overwrite the version with `sparkVersion` JVM property for the supported Spark version (as in the example above).

    Replace `4.2.0` with `4.3.0` in [project/spark-versions.json]({{ uc.github }}/project/spark-versions.json#L6) and you should be able to build Unity Catalog 0.7.0 with Spark 4.3.0. Be careful as you're stepping onto an uncharted territory ☠️

Once the build is finished, you should find the following directories in the local `~/.ivy2` directory.

```shell
ls -l ~/.ivy2/local/io.unitycatalog
```

```text
drwxr-xr-x@ 3 jacek  staff  96 Nov  8 17:02 unitycatalog-client
drwxr-xr-x@ 3 jacek  staff  96 Nov  8 17:02 unitycatalog-hadoop
drwxr-xr-x@ 3 jacek  staff  96 Nov  8 17:02 unitycatalog-server
drwxr-xr-x@ 3 jacek  staff  96 Nov  8 17:02 unitycatalog-spark_4.2_2.13
```

The Spark Connector module is in `unitycatalog-spark_{{ spark.version_short }}_2.13/{{ uc.version }}/jars` directory.

```shell
ls -l ~/.ivy2/local/io.unitycatalog/unitycatalog-spark_{{ spark.version_short }}_2.13/{{ uc.version }}/jars
```

```text
-rw-r--r--@ 1 jacek  staff  119741 Nov  8 17:02 unitycatalog-spark_4.2_2.13.jar
-rw-r--r--@ 1 jacek  staff      32 Nov  8 17:02 unitycatalog-spark_4.2_2.13.jar.md5
-rw-r--r--@ 1 jacek  staff      40 Nov  8 17:02 unitycatalog-spark_4.2_2.13.jar.sha1
```

!!! warning "`~/.ivy2` and `~/.ivy2.5.2`"
    sbt uses `~/.ivy2` directory by default to store dependencies (local and downloaded).
    Apache Spark uses `~/.ivy2.5.2` directory to manage dependencies.

    The dependency names are different, too.

    Copy `unitycatalog-spark_{{ spark.version_short }}_2.13` and the others to `~/.ivy2.5.2/jars/` so the newly-built jars could be picked up.

    ```shell
    cp ~/.ivy2/local/io.unitycatalog/unitycatalog-spark_{{ spark.version_short }}_2.13/{{ uc.version }}/jars/unitycatalog-spark_{{ spark.version_short }}_2.13.jar \
       ~/.ivy2.5.2/jars/io.unitycatalog_unitycatalog-spark_{{ spark.version_short }}_2.13-{{ uc.version }}.jar
    ```

## Run Spark Application with Unity Catalog

This demo re-configures the Spark SQL built-in default two-level-only catalog `spark_catalog` and defines a brand new `unity` catalog.
Both use the very same configuration for simplicity yet serve similar but slightly different purposes.

!!! warning "Apache Spark 4.2.1"
    [Apache Spark 4.2.1](https://spark.apache.org/news/spark-4-2-1-released.html) is not officially supported by [Unity Catalog 0.7.0]({{ uc.github }}/project/spark-versions.json). Use at your own risk.

=== "Spark 4.2.1 + Delta Lake 4.4.1"

    ```shell
    ./bin/spark-shell \
      --packages \
        io.delta:delta-spark_2.13:4.4.1,io.unitycatalog:unitycatalog-spark_{{ spark.version_short }}_2.13:{{ uc.version }},org.slf4j:slf4j-api:2.0.17 \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.spark_catalog.type=static \
      --conf spark.sql.catalog.spark_catalog.token=some_token \
      --conf spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity.type=static \
      --conf spark.sql.catalog.unity.token=some_token
    ```

    ```text
    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /___/ .__/\_,_/_/ /_/\_\   version 4.2.1
          /_/

    Type in expressions to have them evaluated.
    Spark connect server version 4.2.1.
    Spark session available as 'spark'.
    ```

    ```scala
    assert(spark.version == "4.2.1")
    assert(io.delta.VERSION == "4.4.1")
    ```

=== "uv + PySpark 4.2.1 + Delta Lake 4.4.1"

    ```shell
    uvx --from "pyspark==4.2.1" pyspark \
      --packages \
        io.delta:delta-spark_2.13:4.4.1,io.unitycatalog:unitycatalog-spark_{{ spark.version_short }}_2.13:{{ uc.version }},org.slf4j:slf4j-api:2.0.17 \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```

    ```py
    assert(spark.version == "4.2.1")
    ```

## spark_catalog Catalog

### Default Hive Catalog in Spark SQL

The following is a list of the catalogs Unity Catalog comes with and knows about.

```shell
./bin/uc catalog list --output jsonPretty | jq '[.[] | del(..|nulls)]'
```

```json
[
  {
    "name": "unity",
    "comment": "Main catalog",
    "properties": {},
    "created_at": 1721234405334,
    "id": "f029b870-9468-4f10-badc-630b41e5690d"
  }
]
```

There is no `spark_catalog` catalog listed (as it is the default internal Spark SQL catalog).

In the terminal with Spark Shell, execute the following for the list of the catalogs Spark SQL knows about.

```scala
spark.catalog.listDatabases().show(truncate=false)
```

```text
scala> spark.catalog.listDatabases().show(truncate=false)
io.unitycatalog.client.ApiException: listSchemas call failed with: 404 - {"error_code":"CATALOG_NOT_FOUND","details":[{"reason":"CATALOG_NOT_FOUND","@type":"type.googleapis.com/google.rpc.ErrorInfo"}],"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.SchemasApi.getApiException(SchemasApi.java:77)
  at io.unitycatalog.client.api.SchemasApi.listSchemasWithHttpInfo(SchemasApi.java:358)
  at io.unitycatalog.client.api.SchemasApi.listSchemas(SchemasApi.java:334)
  at io.unitycatalog.spark.UCProxy.listNamespaces(UCSingleCatalog.scala:1271)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listNamespaces(DelegatingCatalogExtension.java:147)
  at io.unitycatalog.spark.UCSingleCatalog.listNamespaces(UCSingleCatalog.scala:576)
  at org.apache.spark.sql.execution.command.ShowNamespacesCommand.run(ShowNamespacesCommand.scala:44)
  ...
```

This query failed as the current catalog is the built-in `spark_catalog` which is not known to Unity Catalog.

```scala
assert(spark.catalog.currentCatalog() == "spark_catalog")
```

There are a couple of options to set it up properly (_fix it_):

1. Define a new `spark_catalog` catalog in Unity Catalog.
1. Set the default catalog to be any catalog known to Unity Catalog.
1. Use three-part names for the tables in the `unity` catalog (that is available in Unity Catalog).

### Create spark_catalog Catalog in Unity Catalog

Let's create `spark_catalog` in Unity Catalog.

```shell
./bin/uc catalog create --name spark_catalog
```

```shell
./bin/uc schema create --catalog spark_catalog --name default
```

```shell
./bin/uc table create \
    --full_name spark_catalog.default.uc_demo \
    --columns 'id INT' \
    --storage_location /tmp/uc_demo \
    --format delta
```

```shell
tree /tmp/uc_demo
```

```console
/tmp/uc_demo
└── _delta_log
    └── 00000000000000000000.json

2 directories, 1 file
```

With the `spark_catalog` catalog in Unity Catalog created, we can now list all the available tables in the default Spark catalog.
There should be `uc_demo` table available.

```scala
spark.catalog.listTables().show(truncate=false)
```

```text
+-------+-------------+---------+-----------+---------+-----------+
|name   |catalog      |namespace|description|tableType|isTemporary|
+-------+-------------+---------+-----------+---------+-----------+
|uc_demo|spark_catalog|[default]|NULL       |EXTERNAL |false      |
+-------+-------------+---------+-----------+---------+-----------+
```

Let's change (_write to_) the `uc_demo` delta table that was registered to Unity Catalog.

```scala
spark.range(1).write.insertInto("uc_demo")
```

It works! 🥳

??? danger "Apache Spark 4.3.0 throws Exception"
    Writing data to delta table raises an exception on Spark 4.3.0.

Let's query (_read from_) the `uc_demo` delta table.

```scala
spark.table("uc_demo").show
```

```text
+---+
| id|
+---+
|  0|
+---+
```

## unity Catalog

Unity Catalog is accessible using `unity` catalog ID.

```scala
sql("SET CATALOG unity")
```

```scala
spark.catalog.listCatalogs().show()
```

```text
+-------------+-----------+
|         name|description|
+-------------+-----------+
|spark_catalog|       NULL|
|        unity|       NULL|
+-------------+-----------+
```

```scala
spark.catalog.listDatabases().show()
```

```text
+-------+-------+--------------+-----------+
|   name|catalog|   description|locationUri|
+-------+-------+--------------+-----------+
|default|  unity|Default schema|       NULL|
+-------+-------+--------------+-----------+
```

```scala
assert(spark.catalog.tableExists("unity.default.numbers"))
```

```scala
sql("DESC EXTENDED unity.default.numbers").show(truncate=false)
```

```text
+----------------------------+-----------------------------------------------------------------------------------------+-------+
|col_name                    |data_type                                                                                |comment|
+----------------------------+-----------------------------------------------------------------------------------------+-------+
|as_int                      |int                                                                                      |NULL   |
|as_double                   |double                                                                                   |NULL   |
|                            |                                                                                         |       |
|# Detailed Table Information|                                                                                         |       |
|Catalog                     |unity                                                                                    |       |
|Namespace                   |default                                                                                  |       |
|Database                    |default                                                                                  |       |
|Table                       |numbers                                                                                  |       |
|Type                        |EXTERNAL                                                                                 |       |
|Location                    |file:/Users/jacek/oss/unitycatalog/etc/data/external/unity/default/tables/numbers        |       |
|Provider                    |delta                                                                                    |       |
|Table Properties            |[delta.minReaderVersion=1,delta.minWriterVersion=2,option.key1=value1,option.key2=value2]|       |
+----------------------------+-----------------------------------------------------------------------------------------+-------+
```

```bash
./bin/uc table get --full_name unity.default.numbers
```

```text
┌──────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│               KEY                │                                                                          VALUE                                                                           │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                              │numbers                                                                                                                                                   │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME                      │unity                                                                                                                                                     │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME                       │default                                                                                                                                                   │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_TYPE                        │EXTERNAL                                                                                                                                                  │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_SOURCE_FORMAT                │DELTA                                                                                                                                                     │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COLUMNS                           │{"name":"as_int","type_text":"int","type_json":"{\"name\":\"as_int\",\"type\":\"integer\",\"nullable\":false,\"metadata\":{}}","type_name":"INT","type_pre│
│                                  │cision":0,"type_scale":0,"type_interval_type":null,"position":0,"comment":"Int column","nullable":false,"partition_index":null}                           │
│                                  │{"name":"as_double","type_text":"double","type_json":"{\"name\":\"as_double\",\"type\":\"double\",\"nullable\":false,\"metadata\":{}}","type_name":"DOUBLE│
│                                  │","type_precision":0,"type_scale":0,"type_interval_type":null,"position":1,"comment":"Double column","nullable":false,"partition_index":null}             │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│STORAGE_LOCATION                  │file:///Users/jacek/oss/unitycatalog/etc/data/external/unity/default/tables/numbers                                                                       │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT                           │External table                                                                                                                                            │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES                        │{"key1":"value1","key2":"value2"}                                                                                                                         │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│OWNER                             │null                                                                                                                                                      │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT                        │1721234405617                                                                                                                                             │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_BY                        │null                                                                                                                                                      │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT                        │1721234405617                                                                                                                                             │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_BY                        │null                                                                                                                                                      │
├──────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID                          │32025924-be53-4d67-ac39-501a86046c01                                                                                                                      │
└──────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
