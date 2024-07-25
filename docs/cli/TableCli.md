# TableCli

`TableCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to handle `table` sub-commands.

```console
$ ./bin/uc table --help
Please provide a valid sub-command for table.
Valid sub-commands for table are: read, get, create, list, write, delete
For detailed help on table sub-commands, use bin/uc table <sub-command> --help
```

## Handling Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

Subcommand | Params | Handler
-|-|-
 `write` | `full_name` | [writeTable](#writeTable)
 ... | | &nbsp;

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `table` command

## Write to Delta Table { #writeTable }

```java
String writeTable(
  TemporaryTableCredentialsApi temporaryTableCredentialsApi,
  TablesApi tablesApi,
  JSONObject json)
```

!!! note "Only delta tables supported"
    `writeTable` can only write to delta tables (with `DELTA` format in the catalog).

`writeTable` looks up the [table](../server/TableService.md#getTable) (by the `full_name` parameter).

`writeTable` [requests temporary table credentials](#getTemporaryTableCredentials) for `READ_WRITE` operation on the table.

Only for a delta table, `writeTable` [writes out sample data](DeltaKernelWriteUtils.md#writeSampleDataToDeltaTable).

## Demo: Create, Write Sample Data to and Read from External Delta Table

The demo is prepared in such a way to showcase two features of Unity Catalog at the same time:

1. Create an external delta table (`uc table create`)
1. Write sample data to an external delta table (`uc table write`)
1. Read the delta table using [Unity Catalog CLI](index.md) (`uc table read`)
1. Read the delta table using [Spark Integration](../spark-integration/index.md)

That's why the catalog name is the default Spark SQL catalog `spark_catalog` (not Unity Catalog's `unity`).

### Create spark_catalog in Unity Catalog

=== "SHELL"

    ``` bash
    ./bin/uc catalog create \
        --name spark_catalog
    ```

```text
┌───────────────────────────────┬──────────────────────────────────────────────────────────────┐
│              KEY              │                            VALUE                             │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│NAME                           │spark_catalog                                                 │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│COMMENT                        │null                                                          │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│PROPERTIES                     │{}                                                            │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│CREATED_AT                     │1721933958175                                                 │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│UPDATED_AT                     │null                                                          │
├───────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ID                             │0469f2dd-ecce-498d-8fd9-6c04f333135e                          │
└───────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

### Create Demo Schema

=== "SHELL"

    ``` bash
    ./bin/uc schema create \
        --catalog spark_catalog \
        --name demo
    ```

```text
┌────────────────────┬────────────────────────────────────────┐
│        KEY         │                 VALUE                  │
├────────────────────┼────────────────────────────────────────┤
│NAME                │demo                                    │
├────────────────────┼────────────────────────────────────────┤
│CATALOG_NAME        │spark_catalog                           │
├────────────────────┼────────────────────────────────────────┤
│COMMENT             │null                                    │
├────────────────────┼────────────────────────────────────────┤
│PROPERTIES          │{}                                      │
├────────────────────┼────────────────────────────────────────┤
│FULL_NAME           │spark_catalog.demo                      │
├────────────────────┼────────────────────────────────────────┤
│CREATED_AT          │1721934667143                           │
├────────────────────┼────────────────────────────────────────┤
│UPDATED_AT          │null                                    │
├────────────────────┼────────────────────────────────────────┤
│SCHEMA_ID           │f77e80f4-8c14-4da3-b890-0e27d6af1ef5    │
└────────────────────┴────────────────────────────────────────┘
```

### Create External Delta Table

=== "SHELL"

    ``` bash
    ./bin/uc table create \
        --full_name spark_catalog.demo.delta_table \
        --columns "id INT, name STRING" \
        --storage_location /tmp/delta_table
    ```

```text
Table created successfully at: file:///tmp/delta_table
┌────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────┐
│        KEY         │                                          VALUE                                           │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                │delta_table                                                                               │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME        │spark_catalog                                                                             │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME         │demo                                                                                      │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_TYPE          │EXTERNAL                                                                                  │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_SOURCE_FORMAT  │DELTA                                                                                     │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│COLUMNS             │{"name":"id","type_text":"int","type_json":"{\"name\":\"id\",\"type\":\"integer\",\"nullab│
│                    │le\":true,\"metadata\":{}}","type_name":"INT","type_precision":0,"type_scale":0,"type_inte│
│                    │rval_type":null,"position":0,"comment":null,"nullable":true,"partition_index":null}       │
│                    │{"name":"name","type_text":"string","type_json":"{\"name\":\"name\",\"type\":\"string\",\"│
│                    │nullable\":true,\"metadata\":{}}","type_name":"STRING","type_precision":0,"type_scale":0,"│
│                    │type_interval_type":null,"position":1,"comment":null,"nullable":true,"partition_index":nul│
│                    │l}                                                                                        │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│STORAGE_LOCATION    │file:///tmp/delta_table/                                                                  │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT             │null                                                                                      │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES          │{}                                                                                        │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT          │1721934728723                                                                             │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT          │null                                                                                      │
├────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID            │9ddc7ba3-a2b1-4bad-b358-f9910ca0eaa9                                                      │
└────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Read Delta Table

=== "SHELL"

    ``` bash
    ./bin/uc table read \
        --full_name spark_catalog.demo.delta_table
    ```

```text
┌───────────────────────────────────────┬──────────────────────────────────────┐
│id(integer)                            │name(string)                          │
└───────────────────────────────────────┴──────────────────────────────────────┘
```

### Write Sample Data Out to Delta Table

=== "SHELL"

    ``` bash
    ./bin/uc table write \
        --full_name spark_catalog.demo.delta_table
    ```

```text
Table written to successfully at: file:///tmp/delta_table/
┌────────────────────┬────────────────────────────────────────┐
│        KEY         │                 VALUE                  │
└────────────────────┴────────────────────────────────────────┘
```

### Read Delta Table

=== "SHELL"

    ``` bash
    ./bin/uc table read \
        --full_name spark_catalog.demo.delta_table
    ```

```text
┌───────────────────────────────────────┬──────────────────────────────────────┐
│id(integer)                            │name(string)                          │
├───────────────────────────────────────┼──────────────────────────────────────┤
│1                                      │eoFmOHAqPM                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│2                                      │YGzacYHtUa                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│3                                      │IiaJlcUhgu                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│4                                      │yTiXPwxFvP                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│5                                      │FbHXPqhLyS                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│6                                      │FRLqZGMlKj                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│7                                      │VVdiVyaFsh                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│8                                      │DNSTNQfhXX                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│9                                      │BRXCMWjFsG                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│10                                     │NYucEJZuTK                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│11                                     │USIjlhqNMN                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│12                                     │jNXDZkbRnn                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│13                                     │EiNApsmzaz                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│14                                     │TgfXQtocFo                            │
├───────────────────────────────────────┼──────────────────────────────────────┤
│15                                     │TksgpbjlIW                            │
└───────────────────────────────────────┴──────────────────────────────────────┘
```

### Spark Integration

=== "Spark 3.5.1 + Delta Lake 3.2.0"

    ``` bash
    ./bin/spark-shell \
        --packages \
            io.delta:delta-spark_2.13:3.2.0,io.unitycatalog:unitycatalog-spark:0.2.0-SNAPSHOT \
        --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
        --conf spark.sql.catalog.spark_catalog=io.unitycatalog.connectors.spark.UCSingleCatalog \
        --conf spark.sql.catalog.spark_catalog.uri=http://localhost:8080 \
        --conf spark.sql.catalog.unity=io.unitycatalog.connectors.spark.UCSingleCatalog \
        --conf spark.sql.catalog.unity.uri=http://localhost:8080
    ```
&nbsp;

=== "Spark Shell"

    ```scala
    spark.table("demo.delta_table").show
    ```

```text
+---+----------+
| id|      name|
+---+----------+
|  1|eoFmOHAqPM|
|  2|YGzacYHtUa|
|  3|IiaJlcUhgu|
|  4|yTiXPwxFvP|
|  5|FbHXPqhLyS|
|  6|FRLqZGMlKj|
|  7|VVdiVyaFsh|
|  8|DNSTNQfhXX|
|  9|BRXCMWjFsG|
| 10|NYucEJZuTK|
| 11|USIjlhqNMN|
| 12|jNXDZkbRnn|
| 13|EiNApsmzaz|
| 14|TgfXQtocFo|
| 15|TksgpbjlIW|
+---+----------+
```
