# TableService

`TableService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/tables` | [listTables](#listTables) | <ul><li>catalog_name</li><li>schema_name</li><li>max_results</li><li>page_token</li><li>omit_properties</li><li>omit_columns</ul>
 POST | `/tables` | [createTable](#createTable) | JSON-ified [CreateTable](CreateTable.md)
 GET | `/tables/{full_name}` | [getTable](#getTable) | <ul><li>fullName</li></ul>
 DELETE | `/tables/{full_name}` | [deleteTable](#deleteTable) | <ul><li>fullName</li></ul>

```console
$ http http://localhost:8081/api/2.1/unity-catalog/tables catalog_name==unity schema_name==default | jq '.tables[].name'
"numbers"
"marksheet_uniform"
"marksheet"
```
