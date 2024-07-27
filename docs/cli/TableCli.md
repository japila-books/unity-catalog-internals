# TableCli

`TableCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `table` sub-commands](#handle).

```console
$ ./bin/uc table --help
Please provide a valid sub-command for table.
Valid sub-commands for table are: read, get, create, list, write, delete
For detailed help on table sub-commands, use bin/uc table <sub-command> --help
```

## Handle Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

`handle` creates a `TablesApi` and `TemporaryTableCredentialsApi` (with the given [ApiClient](../client/ApiClient.md)).

Subcommand | Handler | API Handlers
-|-|-
 `create` | [createTable](#createTable) | `TablesApi`<br>
 `delete` | [deleteTable](#deleteTable) | `TablesApi`<br>
 `get` | [getTable](#getTable) | `TablesApi`<br>
 `list` | [listTables](#listTables) | `TablesApi`<br>
 `read` | [readTable](#readTable) | `TablesApi`<br>`TemporaryTableCredentialsApi`
 `write` | [writeTable](#writeTable) | `TablesApi`<br>`TemporaryTableCredentialsApi`

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `table` command

## Create Table { #createTable }

```java
String createTable(
  TablesApi apiClient,
  JSONObject json)
```

`createTable` handles `create` sub-command.

=== "CLI"

    ```bash
    ./bin/uc table create --help
    ```

```text
Usage: bin/uc table create [options]
Required Params:
  --full_name The full name of the table. The full name is the concatenation of the catalog name, schema name, and table/volume name separated by a dot. For example, catalog_name.schema_name.table_name.
  --columns The columns of the table. Each column spec should be in the sql-like format  "column_name column_data_type".Supported data types are BOOLEAN, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, DATE, TIMESTAMP, TIMESTAMP_NTZ, STRING, BINARY, DECIMAL. Multiple columns should be separated by a comma. For example: "id INT, name STRING".
  --storage_location The storage location associated with the table. Need to be specified for external tables.
Optional Params:
  --format The format of the data source. Supported values are DELTA, PARQUET, ORC, JSON, CSV, AVRO and TEXT.
  --properties The properties of the entity. Need to be in json format. For example: "{"key1": "value1", "key2": "value2"}".
```

---

`createTable` takes the `full_name` command-line option (from the given `JSONObject`) and extracts the parts (as if they were given separately).

!!! note
    `createTable` accepts a three-level namespace (`[catalog].[schema].[name]`) only.

!!! note
    The command-line option is `full_name` yet it is removed and replaced by the three parts.

Unless specified, `createTable` sets `table_type` to be `EXTERNAL`.

Unless specified, `createTable` sets `data_source_format` to be `DELTA`.

`createTable` creates a [CreateTable](../server/CreateTable.md):

CreateTable | Value
-|-
 `name` | `name`
 `catalogName` | `catalog_name`
 `schemaName` | `schema_name`
 `columns` | `columns`
 `properties` | `properties`
 `tableType` | `table_type`
 `dataSourceFormat` | `data_source_format`

For `EXTERNAL` table type, `createTable` sets `storage_location` of the `CreateTable` as the value of `storage_location` command-line option and [handleTableStorageLocation](#handleTableStorageLocation).

!!! note "Storage Location"
    Storage locations must start with the following prefixes:

    * `s3://`
    * `file:/`
    * `/` for absolute local filesystem paths

!!! note "External Tables with Local Storage Locations"
    For external tables with non-`s3://` storage locations, `createTable` creates a delta table only.

`createTable` requests the given `TablesApi` client to send the `CreateTable` to the server (that responds with a `TableInfo`).

!!! note
    The `CreateTable` request is sent out as a `POST` request to [`/tables` API endpoint](../server/TableService.md#createTable).

### handleTableStorageLocation { #handleTableStorageLocation }

```java
void handleTableStorageLocation(
  String storageLocation,
  List<ColumnInfo> columnInfos)
```

`handleTableStorageLocation`...FIXME

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
