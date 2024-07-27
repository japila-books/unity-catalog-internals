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
