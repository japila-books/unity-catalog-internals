# TableCli

`TableCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `table` sub-commands](#handle).

```console
$ ./bin/uc table --help
Please provide a valid sub-command for table.
Valid sub-commands for table are: read, get, create, list, write, delete
For detailed help on table sub-commands, use bin/uc table <sub-command> --help
```

!!! note "Read-write support for delta tables only"
    Only delta tables are supported for [read](#readTable) and [write](#writeTable) operations.

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
 `create` | [createTable](#createTable) | `TablesApi`
 `delete` | [deleteTable](#deleteTable) | `TablesApi`
 `get` | [getTable](#getTable) | `TablesApi`
 `list` | [listTables](#listTables) | `TablesApi`
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

=== "Help"

    ```bash
    ./bin/uc table create --help
    ```

```text
Usage: bin/uc table create [options]
Required Params:
  --full_name The full name in the format catalog_name.schema_name for schema, or catalog_name.schema_name.table_name for table/function/volume
  --columns The columns of the table. Each column spec should be in the sql-like format  "column_name column_data_type".Supported data types are BOOLEAN, BYTE, SHORT, INT, LONG, FLOAT, DOUBLE, DATE, TIMESTAMP, TIMESTAMP_NTZ, STRING, BINARY, DECIMAL. Multiple columns should be separated by a comma. For example: "id INT, name STRING".
  --storage_location The storage location associated with the table. Need to be specified for external tables.
Optional Params:
  --server UC Server to connect to. Default is reference server.
  --auth_token PAT token to authorize uc requests.
  --output To indicate CLI output format preference. Supported values are json and jsonPretty.
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

!!! note "No Support for Managed Tables using CLI"
    Only `EXTERNAL` tables are created using `./bin/uc` command-line utility.

Unless specified (using `format` CLI option), `createTable` sets `data_source_format` to be `DELTA`.

`createTable` creates a [CreateTable](../server/CreateTable.md):

CreateTable | Server Param | CLI Option
-|-|-
 `name` | `name` | `name`
 `catalogName` | `catalog_name` | `catalog`
 `schemaName` | `schema_name` | `schema`
 `columns` | `columns` | `columns`
 `properties` | `properties` | `properties`
 `tableType` | `table_type` | `table_type`
 `dataSourceFormat` | `data_source_format` | `format`

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

`handleTableStorageLocation` supports `storageLocation`s with one of the following prefixes (or throws a `CliException`):

* `s3://`
* `file:/`
* `/` for absolute local filesystem paths

For a local filesystem path (a non-`s3://` storage location), `handleTableStorageLocation` [creates an empty delta table](DeltaKernelUtils.md#createDeltaTable) (the directory with a delta log at the storage location).

!!! note "No AwsCredentials Used"
    `handleTableStorageLocation` [creates an empty delta table](DeltaKernelUtils.md#createDeltaTable) with no [AwsCredentials](../server/AwsCredentials.md) (`null`).

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
