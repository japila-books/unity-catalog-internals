---
hide:
- navigation
---

# Demo: Namespace Support in Spark Connector

The demo shows support in Unity Catalog's [Spark Connector](../spark-connector/index.md) for various namespace-related commands (e.g., SHOW NAMESPACES, DESC NAMESPACE).

=== "Spark 3.5.1 + Delta Lake {{ uc.version }}"

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

=== "Spark Shell"

    ```scala
    sql("SET spark.sql.defaultCatalog").show(truncate=false)
    ```

```text
+------------------------+-------------+
|key                     |value        |
+------------------------+-------------+
|spark.sql.defaultCatalog|spark_catalog|
+------------------------+-------------+
```

=== "Spark Shell"

    ```scala
    sql("SELECT current_catalog()").show(truncate=false)
    ```

```text
+-----------------+
|current_catalog()|
+-----------------+
|spark_catalog    |
+-----------------+
```

The following executes [UCSingleCatalog.initialize](../spark-connector/UCSingleCatalog.md#initialize) that in turn creates a [UCProxy](../spark-connector/UCProxy.md).

```scala
assert(spark.sessionState.catalogManager.currentCatalog.isInstanceOf[io.unitycatalog.connectors.spark.UCSingleCatalog])
```

```scala
assert(spark.sessionState.catalogManager.currentCatalog.name == "spark_catalog")
```

`SHOW NAMESPACES` requests the [UCProxy](../spark-connector/UCProxy.md) to [list the namespaces](../spark-connector/UCProxy.md#listNamespaces) with the name of the catalog.
No `IN` clause means the current default catalog.

!!! note
    There is this single `unity` catalog registered in Unity Catalog by default.
    No other catalogs (incl. the default `spark_catalog` in Apache Spark) are available.

=== "Unity Catalog CLI"

    ```shell
    ./bin/uc catalog list
    ```

```text
┌─────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │1721234405334│null      │f029b870-9468-4f10-badc-630b41e5690d│
└─────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

=== "Spark Shell"

    ```scala
    sql("SHOW NAMESPACES").show()
    ```

```text
io.unitycatalog.client.ApiException: listSchemas call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.SchemasApi.getApiException(SchemasApi.java:77)
  at io.unitycatalog.client.api.SchemasApi.listSchemasWithHttpInfo(SchemasApi.java:358)
  at io.unitycatalog.client.api.SchemasApi.listSchemas(SchemasApi.java:334)
  at io.unitycatalog.connectors.spark.UCProxy.listNamespaces(../spark-connector/UCSingleCatalog.scala:218)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listNamespaces(DelegatingCatalogExtension.java:140)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listNamespaces(../spark-connector/UCSingleCatalog.scala:63)
  at org.apache.spark.sql.execution.datasources.v2.ShowNamespacesExec.run(ShowNamespacesExec.scala:42)
  ...
```

Querying `unity` catalog works just fine.

=== "Spark Shell"

    ```scala
    sql("SHOW NAMESPACES IN unity").show()
    ```

```console
+---------+
|namespace|
+---------+
|  default|
+---------+
```

When requested for the [tables](../spark-connector/UCProxy.md#listTables), `UCProxy` uses the name of the catalog (i.e., `spark_catalog`) as the catalog name to talk to the [TableService](../server/TableService.md) for the [table list](../server/TableService.md#listTables).

=== "Spark Shell"

    ```scala
    sql("SHOW TABLES").show(truncate = false)
    ```

```text
io.unitycatalog.client.ApiException: listTables call failed with: 404 - {"error_code":"NOT_FOUND","details":[{"reason":"NOT_FOUND","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"Catalog not found: spark_catalog"}
  at io.unitycatalog.client.api.TablesApi.getApiException(TablesApi.java:76)
  at io.unitycatalog.client.api.TablesApi.listTablesWithHttpInfo(TablesApi.java:342)
  at io.unitycatalog.client.api.TablesApi.listTables(TablesApi.java:317)
  at io.unitycatalog.connectors.spark.UCProxy.listTables(../spark-connector/UCSingleCatalog.scala:129)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.listTables(DelegatingCatalogExtension.java:68)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.listTables(../spark-connector/UCSingleCatalog.scala:38)
  ...
```

=== "Spark Shell"

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

=== "Unity Catalog CLI"

    ```shell
    ./bin/uc catalog list
    ```

    ```console
    ┌─────────────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
    │    NAME     │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
    ├─────────────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
    │spark_catalog│null        │{}        │1722721567116│null      │c3cf6d26-3cba-4071-bdcf-417ecdb45445│
    ├─────────────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
    │unity        │Main catalog│{}        │1721234405334│null      │f029b870-9468-4f10-badc-630b41e5690d│
    └─────────────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
    ```

=== "Spark Shell"

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

There's a tiny bug in Unity Catalog with `DESC NAMESPACE` with just a catalog and no sub-namespace.

=== "Spark Shell"

    ```scala
    sql("DESC NAMESPACE unity").show()
    ```

```text
java.lang.ArrayIndexOutOfBoundsException: Index 0 out of bounds for length 0
  at io.unitycatalog.connectors.spark.UCProxy.loadNamespaceMetadata(../spark-connector/UCSingleCatalog.scala:249)
  at org.apache.spark.sql.connector.catalog.DelegatingCatalogExtension.loadNamespaceMetadata(DelegatingCatalogExtension.java:156)
  at io.unitycatalog.connectors.spark.UCSingleCatalog.loadNamespaceMetadata(../spark-connector/UCSingleCatalog.scala:72)
  ...
```

Let's create a namespace in `unity` catalog.

```text
sql("CREATE NAMESPACE unity.sub_catalog").show()
```

=== "Spark Shell"

    ```scala
    sql("DESC NAMESPACE unity.sub_catalog").show()
    ```

```text
+--------------+-----------+
|     info_name| info_value|
+--------------+-----------+
|  Catalog Name|      unity|
|Namespace Name|sub_catalog|
+--------------+-----------+
```
