# TableRepository

## Persist Table Metadata { #createTable }

```java
TableInfo createTable(
  CreateTable createTable)
```

`createTable` creates a `TableInfo` with randomly-generated UUID as the table ID and the other metadata.

`createTable` prints out the following DEBUG message to the logs:

```text
Creating table: [fullName]
```

!!! danger "`MANAGED` tables are not supported yet"

`createTable` asserts that `storage_location` is specified for an [EXTERNAL](../server/CreateTable.md#EXTERNAL) table.

`createTable` persists the table's [properties](../server/CreateTable.md#properties) (to `uc_properties` table using `PropertyDAO`).

In the end, `createTable` persists the [table metadata](../server/CreateTable.md).

---

`createTable` is used when:

* `TableService` is requested to [create a table metadata](../server/TableService.md#createTable)

## List Tables { #listTables }

```java
ListTablesResponse listTables(
  String catalogName,
  String schemaName,
  Optional<Integer> maxResults,
  Optional<String> pageToken,
  Boolean omitProperties,
  Boolean omitColumns)  // (1)!
ListTablesResponse listTables(
  Session session,
  UUID schemaId,
  String catalogName,
  String schemaName,
  Optional<Integer> maxResults,
  Optional<String> pageToken,
  Boolean omitProperties,
  Boolean omitColumns)
```

1. Opens a new session using the system-wide [SessionFactory](#SESSION_FACTORY) and starts a new transaction

`listTables` requests the [PagedListingHelper](#LISTING_HELPER) to [listEntity](PagedListingHelper.md#listEntity).

`listTables`...FIXME

---

`listTables` is used when:

* `TableService` is requested to [list the tables](../server/TableService.md#listTables)
