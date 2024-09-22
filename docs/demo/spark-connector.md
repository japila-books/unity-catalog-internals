---
hide:
- navigation
---

# Demo: Spark Connector

This demo shows how to set up a Spark application (namely `spark-shell` and `pyspark`) with Unity Catalog using the [Spark Connector](../spark-connector/index.md) module.

## Build Spark Connector

Build the Spark Connector module.

``` shell
build/sbt '++2.13' clean package publishLocal spark/publishLocal
```

!!! note "Scala 2.13"
    This demo uses the Scala 2.13 builds of Apache Spark, Delta Lake and Unity Catalog.

    Unless you built Apache Spark with Scala 2.13, replace any `2.13` in this demo with `2.12`.

    Use `spark-shell --version` or `pyspark --version` to learn about your Spark build:

    ```text
    ❯ ./bin/pyspark --version
    Welcome to
        ____              __
        / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
    /___/ .__/\_,_/_/ /_/\_\   version 3.5.2
        /_/

    Using Scala version 2.13.8, OpenJDK 64-Bit Server VM, 17.0.12
    Branch heads/v3.5.2
    Compiled by user jacek on 2024-08-19T17:24:05Z
    Revision a26a80208d7c96b3e3e898f137a05d69cba759d6
    Url <https://github.com/apache/spark.git>
    Type --help for more information.
    ```

Once the build is finished, you should find the following directories in the local `~/.ivy2` directory.

```text
❯ ls -l ~/.ivy2/local/io.unitycatalog
total 0
drwxr-xr-x@ 3 jacek  staff  96 Sep 22 18:53 unitycatalog-client
drwxr-xr-x@ 3 jacek  staff  96 Sep 22 18:53 unitycatalog-server
drwxr-xr-x@ 3 jacek  staff  96 Sep 22 18:53 unitycatalog-spark_2.13
```

The Spark Connector module is under `unitycatalog-spark_2.13/{{ uc.version }}/jars` directory.

## Run Spark Application with Unity Catalog

=== "Spark {{ spark3.version }} + Delta Lake {{ delta3.version }}"

    ``` shell
    ./bin/spark-shell \
      --packages \
        io.delta:delta-spark_{{ scala.version }}:{{ delta3.version }},io.unitycatalog:unitycatalog-spark_{{ scala.version }}:{{ uc.version }} \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```

    ``` text
    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /___/ .__/\_,_/_/ /_/\_\   version 3.5.2
          /_/
    
    Using Scala version 2.13.8 (OpenJDK 64-Bit Server VM, Java 17.0.12)
    ```

    ``` text
    scala> assert(spark.version == "{{ spark3.version }}")
    scala> assert(io.delta.VERSION == "{{ delta3.version }}")
    ```

=== "PySpark {{ spark3.version }} + Delta Lake {{ delta3.version }}"

    ``` shell
    ./bin/pyspark \
      --packages \
        io.delta:delta-spark_{{ scala.version }}:{{ delta3.version }},io.unitycatalog:unitycatalog-spark_{{ scala.version }}:{{ uc.version }} \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```

    ``` text
    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /__ / .__/\_,_/_/ /_/\_\   version 3.5.2
          /_/
    
    Using Python version 3.9.16 (main, May 15 2023 18:51:40)
    ```

=== "Spark {{ spark4.version }} + Delta Lake {{ delta4.version }}"

    Download Apache Spark {{ spark4.version }} from [Preview release of Spark 4.0](https://spark.apache.org/news/spark-4.0.0-preview1.html).

    ``` shell
    ./bin/spark-shell \
      --conf spark.jars.ivy=$HOME/.ivy2 \
      --packages \
        io.delta:delta-spark_{{ scala.version }}:{{ delta4.version }},io.unitycatalog:unitycatalog-spark_{{ scala.version }}:{{ uc.version }} \
      --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
      --conf spark.sql.catalog.spark_catalog=io.unitycatalog.connectors.spark.UCSingleCatalog \
      --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
      --conf spark.sql.catalog.unity=io.unitycatalog.connectors.spark.UCSingleCatalog \
      --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```

    ``` text
    Welcome to
          ____              __
        / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
      /___/ .__/\_,_/_/ /_/\_\   version 4.0.0-preview1
          /_/

    Using Scala version 2.13.14 (OpenJDK 64-Bit Server VM, Java 17.0.11)
    ```

    ```scala
    assert(spark4.version == "{{ spark4.version }}", "Unity Catalog {{ uc.version }} supports Apache Spark {{ spark4.version }} only")
    assert(io.delta4.version == "{{ delta4.version }}", "Unity Catalog {{ uc.version }} supports Delta Lake {{ delta4.version }} only")
    ```

## Default spark_catalog

The following is a list of the catalogs Unity Catalog comes with and knows about.

``` console
$ ./bin/uc catalog list
┌─────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │1720429531248│null      │f68e0329-d510-4558-b984-457218f573d9│
└─────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

There is no `spark_catalog` catalog listed (as it is the default internal Spark SQL catalog).

The following is a list of the catalogs Spark SQL knows about.

``` scala
spark.catalog.listCatalogs().show()
```

``` text
+-------------+-----------+
|         name|description|
+-------------+-----------+
|spark_catalog|       NULL|
+-------------+-----------+
```

There is the default `spark_catalog` catalog (but no Unity Catalog-specific `unity` catalog).

``` scala
spark.catalog.listDatabases().show()
```

``` text
+----+-------------+-----------+-----------+
|name|      catalog|description|locationUri|
+----+-------------+-----------+-----------+
|demo|spark_catalog|       NULL|       NULL|
+----+-------------+-----------+-----------+
```

``` scala
assert(spark.catalog.currentCatalog() == "spark_catalog")
```

``` scala
spark.catalog.setCurrentCatalog("unity")
```

``` text
scala> spark.catalog.listTables("default")
io.unitycatalog.client.ApiException: listTables call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Schema not found: default"}
  at io.unitycatalog.client.api.TablesApi.getApiException(TablesApi.java:76)
  at io.unitycatalog.client.api.TablesApi.listTablesWithHttpInfo(TablesApi.java:342)
  at io.unitycatalog.client.api.TablesApi.listTables(TablesApi.java:317)
  at io.unitycatalog.spark.UCProxy.listTables(UCSingleCatalog.scala:168)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listTables(DelegatingCatalogExtension.java:68)
  at io.unitycatalog.spark.UCSingleCatalog.listTables(UCSingleCatalog.scala:52)
...
```

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
❯ tree /tmp/uc_demo
/tmp/uc_demo
└── _delta_log
    └── 00000000000000000000.json

2 directories, 1 file
```

``` scala
scala> spark.catalog.listTables()
org.apache.spark.sql.catalyst.parser.ParseException:
[PARSE_SYNTAX_ERROR] Syntax error at or near end of input.(line 1, pos 0)

== SQL ==

^^^

  at org.apache.spark.sql.catalyst.parser.ParseException.withCommand(parsers.scala:257)
  at org.apache.spark.sql.catalyst.parser.AbstractParser.parse(parsers.scala:98)
  at org.apache.spark.sql.execution.SparkSqlParser.parse(SparkSqlParser.scala:54)
  at org.apache.spark.sql.catalyst.parser.AbstractSqlParser.parseMultipartIdentifier(AbstractSqlParser.scala:54)
  at io.delta.sql.parser.DeltaSqlParser.parseMultipartIdentifier(DeltaSqlParser.scala:153)
  at org.apache.spark.sql.internal.CatalogImpl.parseIdent(CatalogImpl.scala:51)
  at org.apache.spark.sql.internal.CatalogImpl.resolveNamespace(CatalogImpl.scala:427)
  at org.apache.spark.sql.internal.CatalogImpl.listTablesInternal(CatalogImpl.scala:143)
  at org.apache.spark.sql.internal.CatalogImpl.listTables(CatalogImpl.scala:127)
  at org.apache.spark.sql.internal.CatalogImpl.listTables(CatalogImpl.scala:118)
  ... 42 elided
```

Switch back to `spark_catalog` catalog.

``` scala
sql("SET CATALOG spark_catalog")
```

We've registered an empty `uc_demo` table in Unity Catalog already.

``` scala
assert(spark.catalog.tableExists("uc_demo"))
```

It was equivalent to the following query:

``` scala
assert(spark.catalog.tableExists("default.uc_demo"))
```

Let's change (_write to_) the `uc_demo` delta table that was registered to Unity Catalog.

``` scala
sql("INSERT INTO uc_demo(id) VALUES (1)").show(truncate=false)
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
|  1|
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
|Location                    |file:/Users/jacek/dev/oss/unitycatalog/etc/data/external/unity/default/tables/numbers    |       |
|Provider                    |delta                                                                                    |       |
|Table Properties            |[delta.minReaderVersion=1,delta.minWriterVersion=2,option.key1=value1,option.key2=value2]|       |
+----------------------------+-----------------------------------------------------------------------------------------+-------+
```

``` bash
./bin/uc table get --full_name unity.default.numbers
```

``` text
┌───────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│              KEY              │                                                                    VALUE                                                                    │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                           │numbers                                                                                                                                      │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME                   │unity                                                                                                                                        │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME                    │default                                                                                                                                      │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_TYPE                     │EXTERNAL                                                                                                                                     │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_SOURCE_FORMAT             │DELTA                                                                                                                                        │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COLUMNS                        │{"name":"as_int","type_text":"int","type_json":"{\"name\":\"as_int\",\"type\":\"integer\",\"nullable\":false,\"metadata\":{}}","type_name":"I│
│                               │NT","type_precision":0,"type_scale":0,"type_interval_type":null,"position":0,"comment":"Int column","nullable":false,"partition_index":null} │
│                               │{"name":"as_double","type_text":"double","type_json":"{\"name\":\"as_double\",\"type\":\"double\",\"nullable\":false,\"metadata\":{}}","type_│
│                               │name":"DOUBLE","type_precision":0,"type_scale":0,"type_interval_type":null,"position":1,"comment":"Double                                    │
│                               │column","nullable":false,"partition_index":null}                                                                                             │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│STORAGE_LOCATION               │file:///Users/jacek/dev/oss/unitycatalog/etc/data/external/unity/default/tables/numbers/                                                     │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT                        │External table                                                                                                                               │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES                     │{"key1":"value1","key2":"value2"}                                                                                                            │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│OWNER                          │null                                                                                                                                         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT                     │1721234405617                                                                                                                                │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_BY                     │null                                                                                                                                         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT                     │1721234405617                                                                                                                                │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_BY                     │null                                                                                                                                         │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID                       │32025924-be53-4d67-ac39-501a86046c01                                                                                                         │
└───────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
