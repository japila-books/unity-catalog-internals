# Spark Integration

Unity Catalog supports Apache Spark and Delta Lake using [UCSingleCatalog](UCSingleCatalog.md) and [UCProxy](UCProxy.md).

The following features are supported:

* Read/write (partitioned) external parquet tables
* Read/write (partitioned) external delta tables
* Support the path table syntax of delta tables
* [Temporary credentials for secured access](./UCProxy.md#loadTable) to local and S3 tables ([parquet tables only, no delta tables yet]({{ uc.commit }}/681acbdb46f375d00e402739bc3ea31fc407e732))
* [Namespace](#namespace-support)

## Namespace Support

As of [this commit]({{ uc.commit }}/10c57d14d2af5e208f6e15f06df4950b6d587ba1), Unity Catalog supports various namespace-related commands (e.g., `SHOW NAMESPACES`, `DESC NAMESPACE`).

=== "Spark 3.5.1 + Delta Lake 3.2.0"

    ``` shell
    SPARK_SUBMIT_OPTS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5555 \
    ./bin/spark-shell \
      --packages \
        io.delta:delta-spark_2.13:3.2.0,io.unitycatalog:unitycatalog-spark:{{ uc.version }} \
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
      /___/ .__/\_,_/_/ /_/\_\   version 3.5.1
          /_/

    Using Scala version 2.13.8 (OpenJDK 64-Bit Server VM, Java 17.0.12)
    ```

```text
scala> sql("SET spark.sql.defaultCatalog").show(truncate=false)
+------------------------+-------------+
|key                     |value        |
+------------------------+-------------+
|spark.sql.defaultCatalog|spark_catalog|
+------------------------+-------------+
```

```text
scala> sql("SELECT current_catalog()").show(truncate=false)
+-----------------+
|current_catalog()|
+-----------------+
|spark_catalog    |
+-----------------+
```

The following executes [UCSingleCatalog.initialize](UCSingleCatalog.md#initialize) that in turn creates a [UCProxy](UCProxy.md).

```scala
assert(spark.sessionState.catalogManager.currentCatalog.isInstanceOf[io.unitycatalog.connectors.spark.UCSingleCatalog])
```

```scala
assert(spark.sessionState.catalogManager.currentCatalog.name == "spark_catalog")
```

`SHOW NAMESPACES` requests the [UCProxy](UCProxy.md) to [listNamespaces](UCProxy.md#listNamespaces) with the name of the catalog.
No `IN` clause means the current default catalog.

!!! note
    There is `unity` catalog registered in Unity Catalog by default. No other catalogs (incl. the default `spark_catalog` in Apache Spark) are available.

```console
$ ./bin/uc catalog list
┌─────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │1721234405334│null      │f029b870-9468-4f10-badc-630b41e5690d│
└─────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

```text
scala> sql("SHOW NAMESPACES").show()
io.unitycatalog.client.ApiException: listSchemas call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.SchemasApi.getApiException(SchemasApi.java:77)
  at io.unitycatalog.client.api.SchemasApi.listSchemasWithHttpInfo(SchemasApi.java:358)
  at io.unitycatalog.client.api.SchemasApi.listSchemas(SchemasApi.java:334)
  at io.unitycatalog.connectors.spark.UCProxy.listNamespaces(UCSingleCatalog.scala:218)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listNamespaces(DelegatingCatalogExtension.java:140)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listNamespaces(UCSingleCatalog.scala:63)
  at org.apache.spark.sql.execution.datasources.v2.ShowNamespacesExec.run(ShowNamespacesExec.scala:42)
  ...
```

Querying `unity` catalog works just fine.

```console
scala> sql("SHOW NAMESPACES IN unity").show()
+---------+
|namespace|
+---------+
|  default|
+---------+
```

When requested for the [tables](UCProxy.md#listTables), `UCProxy` uses the name of the catalog (i.e., `spark_catalog`) as the catalog name to talk to the [TableService](../server/TableService.md) for the [table list](#listTables).

```text
scala> sql("SHOW TABLES").show(truncate = false)
io.unitycatalog.client.ApiException: listTables call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.TablesApi.getApiException(TablesApi.java:76)
  at io.unitycatalog.client.api.TablesApi.listTablesWithHttpInfo(TablesApi.java:342)
  at io.unitycatalog.client.api.TablesApi.listTables(TablesApi.java:317)
  at io.unitycatalog.connectors.spark.UCProxy.listTables(UCSingleCatalog.scala:129)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listTables(DelegatingCatalogExtension.java:68)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listTables(UCSingleCatalog.scala:38)
  ...
```

=== "Scala"

    ```scala
    sql("SHOW TABLES IN unity.default").show(truncate = false)
    ```

```text
+---------+-----------------+-----------+
|namespace|tableName        |isTemporary|
+---------+-----------------+-----------+
|default  |marksheet        |false      |
|default  |marksheet_uniform|false      |
|default  |numbers          |false      |
|default  |user_countries   |false      |
+---------+-----------------+-----------+
```

Let's define `spark_catalog` in Unity Catalog (to match Spark SQL's session catalog).

```shell
./bin/uc catalog create --name spark_catalog
```

```console
$ ./bin/uc catalog list
┌─────────────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│    NAME     │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────────────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│spark_catalog│null        │{}        │1722721567116│null      │c3cf6d26-3cba-4071-bdcf-417ecdb45445│
├─────────────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity        │Main catalog│{}        │1721234405334│null      │f029b870-9468-4f10-badc-630b41e5690d│
└─────────────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

```text
scala> sql("SHOW NAMESPACES").show()
+---------+
|namespace|
+---------+
+---------+
```

```text
scala> sql("DESC NAMESPACE unity").show()
java.lang.ArrayIndexOutOfBoundsException: Index 0 out of bounds for length 0
  at io.unitycatalog.connectors.spark.UCProxy.loadNamespaceMetadata(UCSingleCatalog.scala:249)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.loadNamespaceMetadata(DelegatingCatalogExtension.java:156)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.loadNamespaceMetadata(UCSingleCatalog.scala:72)
  ...
```

```text
sql("CREATE NAMESPACE unity.sub_catalog").show()
```

```text
scala> sql("DESC NAMESPACE unity.sub_catalog").show()
+--------------+-----------+
|     info_name| info_value|
+--------------+-----------+
|  Catalog Name|      unity|
|Namespace Name|sub_catalog|
+--------------+-----------+
```

=== "Scala"

    ```scala
    sql("SHOW CATALOGS").show()
    ```

```text
+-------------+
|      catalog|
+-------------+
|spark_catalog|
|        unity|
+-------------+
```

## Demo

Build the Spark Integration module.

``` shell
build/sbt clean package publishLocal spark/publishLocal
```

=== "Spark {{ spark.version }} + Delta Lake {{ delta.version }}"

    Download Apache Spark {{ spark.version }} from [Preview release of Spark 4.0](https://spark.apache.org/news/spark-4.0.0-preview1.html).

    ``` shell
    ./bin/spark-shell \
      --conf spark.jars.ivy=$HOME/.ivy2 \
      --packages \
        io.delta:delta-spark_2.13:{{ delta.version }},io.unitycatalog:unitycatalog-spark:{{ uc.version }} \
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
    assert(spark.version == "{{ spark.version }}", "Unity Catalog {{ uc.version }} supports Apache Spark {{ spark.version }} only")
    assert(io.delta.VERSION == "{{ delta.version }}", "Unity Catalog {{ uc.version }} supports Delta Lake {{ delta.version }} only")
    ```

=== "Spark 3.5.1 + Delta Lake 3.2.0"

    ``` shell
    ./bin/spark-shell \
      --packages \
        io.delta:delta-spark_2.13:3.2.0,io.unitycatalog:unitycatalog-spark:{{ uc.version }} \
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
      /___/ .__/\_,_/_/ /_/\_\   version 3.5.1
          /_/

    Using Scala version 2.13.8 (OpenJDK 64-Bit Server VM, Java 17.0.12)
    ```

### spark_catalog

The following is a list of the catalogs Unity Catalog comes with and knows about.

``` console
$ ./bin/uc catalog list
┌─────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │1720429531248│null      │f68e0329-d510-4558-b984-457218f573d9│
└─────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

There is no `spark_catalog` catalog.

The following is a list of the catalogs Spark SQL knows about.

``` text
scala> spark.catalog.listCatalogs.show
+-------------+-----------+
|name         |description|
+-------------+-----------+
|spark_catalog|NULL       |
+-------------+-----------+
```

There is the default `spark_catalog` catalog (and no `unity` catalog).

``` text
scala> spark.catalog.listDatabases()
org.apache.spark.sql.AnalysisException: Catalog spark_catalog does not support namespaces.
  at org.apache.spark.sql.errors.QueryCompilationErrors$.missingCatalogAbilityError(QueryCompilationErrors.scala:1952)
  at org.apache.spark.sql.connector.catalog.CatalogV2Implicits$CatalogHelper.asNamespaceCatalog(CatalogV2Implicits.scala:96)
  at org.apache.spark.sql.execution.datasources.v2.DataSourceV2Strategy.apply(DataSourceV2Strategy.scala:402)
...
```

``` scala
assert(spark.catalog.currentCatalog == "spark_catalog")
```

``` scala
spark.catalog.setCurrentCatalog("unity")
```

``` text
scala> spark.catalog.listTables("default")
{"ts":"2024-07-16T16:08:20.558Z","level":"INFO","msg":"0: get_database: default","logger":"HiveMetaStore"}
{"ts":"2024-07-16T16:08:20.558Z","level":"INFO","msg":"ugi=jacek\tip=unknown-ip-addr\tcmd=get_database: default\t","logger":"audit"}
scala.NotImplementedError: an implementation is missing
  at scala.Predef$.$qmark$qmark$qmark(Predef.scala:344)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listTables(UCSingleCatalog.scala:37)
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
./bin/uc table create --full_name spark_catalog.default.uc_demo --columns 'id INT' --storage_location /tmp/uc_demo --format delta
```

``` console
$ tree /tmp/uc_demo
/tmp/uc_demo
├── _delta_log
│   ├── 00000000000000000000.json
│   ├── 00000000000000000001.json
│   └── 00000000000000000002.json
├── part-00000-bcbbf49f-d038-4001-bdb8-f0983fff3af7-c000.snappy.parquet
└── part-00000-e04f4c07-c6fb-45fe-b760-14bd1835abac-c000.snappy.parquet

2 directories, 5 files
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

It works!

Let's query (_read from_) the `uc_demo` delta table.

``` text
scala> spark.table("uc_demo").show
+---+
| id|
+---+
|  1|
+---+
```

### unity Catalog

Unity Catalog is accessible using `unity` catalog ID.

```scala
sql("SET CATALOG unity")
```

``` text
scala> spark.catalog.listCatalogs.show
+-------------+-----------+
|         name|description|
+-------------+-----------+
|spark_catalog|       NULL|
|        unity|       NULL|
+-------------+-----------+
```

``` text
scala> spark.catalog.listDatabases()
org.apache.spark.sql.AnalysisException: Catalog unity does not support namespaces.
  at org.apache.spark.sql.errors.QueryCompilationErrors$.missingCatalogAbilityError(QueryCompilationErrors.scala:2059)
  at org.apache.spark.sql.connector.catalog.CatalogV2Implicits$CatalogHelper.asNamespaceCatalog(CatalogV2Implicits.scala:115)
  at org.apache.spark.sql.execution.datasources.v2.DataSourceV2Strategy.apply(DataSourceV2Strategy.scala:405)
  ...
```

``` text
assert(spark.catalog.tableExists("unity.default.numbers"))
```

``` text
scala> sql("DESC EXTENDED unity.default.numbers").show(truncate=false)
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

``` text
$ ./bin/uc table get --full_name unity.default.numbers

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
│CREATED_AT                     │1720429531453                                                                                                                                │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT                     │1720429531453                                                                                                                                │
├───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID                       │b5d6db68-5eca-485c-be5f-5f53d4f27f60                                                                                                         │
└───────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
