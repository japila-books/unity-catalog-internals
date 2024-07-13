# TableService

`TableService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/tables` | [listTables](#listTables) | <ul><li>catalog_name<li>schema_name<li>max_results<li>page_token<li>omit_properties<li>omit_columns</ul>
 POST | `/tables` | [createTable](#createTable) | JSON-ified [CreateTable](CreateTable.md)
 GET | `/tables/{full_name}` | [getTable](#getTable) | <ul><li>fullName</ul>
 DELETE | `/tables/{full_name}` | [deleteTable](#deleteTable) | <ul><li>fullName</ul>

```console
$ http http://localhost:8081/api/2.1/unity-catalog/tables catalog_name==unity schema_name==default | jq '.tables[].name'
"numbers"
"marksheet_uniform"
"marksheet"
```

## Creating Table Metadata { #createTable }

```java
HttpResponse createTable(
  CreateTable createTable)
```

`createTable` requests the system-wide [TableRepository](#TABLE_REPOSITORY) instance to [persist](../persistent-storage/TableRepository.md#createTable) the given [table metadata](CreateTable.md).
