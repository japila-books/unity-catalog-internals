# TableService

`TableService` is an API service of [UnityCatalogServer](UnityCatalogServer.md) to handle HTTP requests at `/api/2.1/unity-catalog/tables` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/` | [listTables](#listTables) | <ul><li>catalog_name<li>schema_name<li>max_results<li>page_token<li>omit_properties<li>omit_columns</ul>
 POST | `/` | [createTable](#createTable) | JSON-ified [CreateTable](CreateTable.md)
 GET | `/{full_name}` | [getTable](#getTable) | <ul><li>fullName</ul>
 DELETE | `/{full_name}` | [deleteTable](#deleteTable) | <ul><li>fullName</ul>

```console
$ http http://localhost:8081/api/2.1/unity-catalog/tables catalog_name==unity schema_name==default | jq '.tables[].name'
"numbers"
"marksheet_uniform"
"marksheet"
```

## Creating Instance

`TableService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)

While being created, `TableService` creates an [UnityAccessEvaluator](#evaluator).

`TableService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## UnityAccessEvaluator { #evaluator }

`TableService` creates an [UnityAccessEvaluator](../server-authorization/UnityAccessEvaluator.md) (with the given [UnityCatalogAuthorizer](#authorizer)) when [created](#creating-instance).

## Create Table Metadata { #createTable }

```java
HttpResponse createTable(
  CreateTable createTable)
```

`createTable` handles `POST` requests with the following [AuthorizeKeys](../server-authorization/AuthorizeKeys.md):

Value | Key
-|-
 `SCHEMA` | `schema_name`
 `CATALOG` | `catalog_name`

---

`createTable` requests the system-wide [TableRepository](#TABLE_REPOSITORY) instance to [persist](../persistent-storage/TableRepository.md#createTable) the given [table metadata](CreateTable.md).

## List Tables { #listTables }

```java
HttpResponse listTables(
  String catalogName,
  String schemaName,
  Optional<Integer> maxResults,
  Optional<String> pageToken,
  Optional<Boolean> omitProperties,
  Optional<Boolean> omitColumns)
```

`listTables` requests the system-wide [TableRepository](#TABLE_REPOSITORY) instance to [list the tables](../persistent-storage/TableRepository.md#listTables).
