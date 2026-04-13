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
./build/sbt -DsparkVersion=4.1.1 clean package publishLocal
```

??? note "sparkVersion"
    Unity Catalog builds with Apache Spark 4.0.0 by default.
    You can overwrite the version with `sparkVersion` JVM property (as in the example above).

Once the build is finished, you should find the following directories in the local `~/.ivy2` directory.

```text
$ ls -l ~/.ivy2/local/io.unitycatalog
total 0
drwxr-xr-x@ 3 jacek  staff  96 Apr 13 19:21 unitycatalog-client
drwxr-xr-x@ 3 jacek  staff  96 Apr 13 19:21 unitycatalog-server
drwxr-xr-x@ 3 jacek  staff  96 Apr 13 19:21 unitycatalog-spark_2.13
```

The Spark Connector module is in `unitycatalog-spark_2.13/{{ uc.version }}/jars` directory.

```text
$ ls -l ~/.ivy2/local/io.unitycatalog/unitycatalog-spark_2.13/0.4.1/jars
total 168
-rw-r--r--@ 1 jacek  staff  75192 Apr 13 19:21 unitycatalog-spark_2.13.jar
-rw-r--r--@ 1 jacek  staff     32 Apr 13 19:21 unitycatalog-spark_2.13.jar.md5
-rw-r--r--@ 1 jacek  staff     40 Apr 13 19:21 unitycatalog-spark_2.13.jar.sha1
```

!!! warning "`~/.ivy2` and `~/.ivy2.5.2`"
    sbt uses `~/.ivy2` directory by default to store dependencies (local and downloaded).
    Apache Spark uses `~/.ivy2.5.2` directory to manage dependencies.

    The dependency names are different, too.

    Copy `unitycatalog-spark_2.13.jar` and the others to `~/.ivy2.5.2/jars/` so the newly-built jars could be picked up.

    ```shell
    cp ~/.ivy2/local/io.unitycatalog/unitycatalog-spark_2.13/{{ uc.version }}/jars/unitycatalog-spark_2.13.jar \
       ~/.ivy2.5.2/jars/io.unitycatalog_unitycatalog-spark_2.13-{{ uc.version }}.jar
    ```

## Run Spark Application with Unity Catalog

This demo re-configures the Spark SQL built-in default two-level-only catalog `spark_catalog` and defines a brand new `unity` catalog.
Both use the very same configuration for simplicity yet serve similar but slightly different purposes.

=== "Spark {{ spark.version }} + Delta Lake {{ delta.version }}"

    ``` shell
    ./bin/spark-shell \
      --packages \
        io.delta:delta-spark_2.13:{{ delta.version }},io.unitycatalog:unitycatalog-spark_2.13:{{ uc.version }},org.slf4j:slf4j-api:2.0.17 \
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

    ``` text
    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /___/ .__/\_,_/_/ /_/\_\   version 4.1.1
          /_/

    Using Scala version 2.13.17 (OpenJDK 64-Bit Server VM, Java 17.0.18)
    ```

    ```scala
    assert(spark.version == "{{ spark.version }}")
    assert(io.delta.VERSION == "{{ delta.version }}")
    ```

=== "uv + PySpark {{ spark.version }} + Delta Lake {{ delta.version }}"

    ``` shell
    uvx --from "pyspark=={{ spark.version }}" pyspark \
      --packages \
        io.delta:delta-spark_2.13:{{ delta.version }},io.unitycatalog:unitycatalog-spark_2.13:{{ uc.version }},org.slf4j:slf4j-api:2.0.17 \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```

    ```py
    assert(spark.version == "4.1.1")
    ```

## spark_catalog Catalog

### Default Hive Catalog in Spark SQL

The following is a list of the catalogs Unity Catalog comes with and knows about.

``` console
$ ./bin/uc catalog list
┌─────┬────────────┬──────────┬─────┬─────────────┬──────────┬──────────┬──────────┬────────────────────────────────────┬────────────┬────────────────┐
│NAME │  COMMENT   │PROPERTIES│OWNER│ CREATED_AT  │CREATED_BY│UPDATED_AT│UPDATED_BY│                 ID                 │STORAGE_ROOT│STORAGE_LOCATION│
├─────┼────────────┼──────────┼─────┼─────────────┼──────────┼──────────┼──────────┼────────────────────────────────────┼────────────┼────────────────┤
│unity│Main catalog│{}        │null │1721234405334│null      │null      │null      │f029b870-9468-4f10-badc-630b41e5690d│null        │null            │
└─────┴────────────┴──────────┴─────┴─────────────┴──────────┴──────────┴──────────┴────────────────────────────────────┴────────────┴────────────────┘
```

There is no `spark_catalog` catalog listed (as it is the default internal Spark SQL catalog).

The following is a list of the catalogs Spark SQL knows about.

``` scala
spark.catalog.listDatabases().show(truncate=false)
```

```text
scala> spark.catalog.listDatabases().show(truncate=false)
io.unitycatalog.client.ApiException: listSchemas call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.SchemasApi.getApiException(SchemasApi.java:77)
  at io.unitycatalog.client.api.SchemasApi.listSchemasWithHttpInfo(SchemasApi.java:358)
  at io.unitycatalog.client.api.SchemasApi.listSchemas(SchemasApi.java:334)
  at io.unitycatalog.spark.UCProxy.listNamespaces(UCSingleCatalog.scala:825)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listNamespaces(DelegatingCatalogExtension.java:140)
  at io.unitycatalog.spark.UCSingleCatalog.listNamespaces(UCSingleCatalog.scala:335)
  at org.apache.spark.sql.execution.command.ShowNamespacesCommand.run(ShowNamespacesCommand.scala:44)
  ...
```

This query failed as the current catalog is the built-in `spark_catalog` that is not known to Unity Catalog.

``` scala
assert(spark.catalog.currentCatalog() == "spark_catalog")
```

There are a couple of options to set it up properly (_fix it_):

1. Define a new `spark_catalog` catalog in Unity Catalog.
1. Set the default catalog to be any catalog known to Unity Catalog.
1. Use three-part names for the tables in the `unity` catalog (that is available in Unity Catalog).

### Create spark_catalog Catalog in Unity Catalog

Let's create `spark_catalog` in Unity Catalog.

``` shell
./bin/uc catalog create --name spark_catalog
```

``` shell
./bin/uc schema create --catalog spark_catalog --name default
```

``` shell
./bin/uc table create \
    --full_name spark_catalog.default.uc_demo \
    --columns 'id INT' \
    --storage_location /tmp/uc_demo \
    --format delta
```

``` console
$ tree /tmp/uc_demo
/tmp/uc_demo
└── _delta_log
    └── 00000000000000000000.json

2 directories, 1 file
```

Let's list all the available tables in `spark_catalog` catalog in Unity Catalog.
There should be `uc_demo` table available.

``` scala
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

``` scala
spark.range(1).write.insertInto("uc_demo")
```

It works! 🥳

Let's query (_read from_) the `uc_demo` delta table.

``` scala
spark.table("uc_demo").show
```

``` text
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

``` scala
spark.catalog.listCatalogs().show()
```

``` text
+-------------+-----------+
|         name|description|
+-------------+-----------+
|spark_catalog|       NULL|
|        unity|       NULL|
+-------------+-----------+
```

``` scala
spark.catalog.listDatabases().show()
```

``` text
+-------+-------+--------------+-----------+
|   name|catalog|   description|locationUri|
+-------+-------+--------------+-----------+
|default|  unity|Default schema|       NULL|
+-------+-------+--------------+-----------+
```

``` scala
assert(spark.catalog.tableExists("unity.default.numbers"))
```

``` scala
sql("DESC EXTENDED unity.default.numbers").show(truncate=false)
```

``` text
+----------------------------+-----------------------------------------------------------------------------------------+-------+
|col_name                    |data_type                                                                                |comment|
+----------------------------+-----------------------------------------------------------------------------------------+-------+
|as_int                      |int                                                                                      |NULL   |
|as_double                   |double                                                                                   |NULL   |
|                            |                                                                                         |       |
|# Detailed Table Information|                                                                                         |       |
|Name                        |unity.default.numbers                                                                    |       |
|Type                        |EXTERNAL                                                                                 |       |
|Location                    |file:/Users/jacek/oss/unitycatalog/etc/data/external/unity/default/tables/numbers        |       |
|Provider                    |delta                                                                                    |       |
|Table Properties            |[delta.minReaderVersion=1,delta.minWriterVersion=2,option.key1=value1,option.key2=value2]|       |
+----------------------------+-----------------------------------------------------------------------------------------+-------+
```

``` bash
./bin/uc table get --full_name unity.default.numbers
```

``` text
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
