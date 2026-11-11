---
title: IcebergRestCatalogService
---

# IcebergRestCatalogService &mdash; Apache Iceberg REST APIs

`IcebergRestCatalogService` is a [Unity Catalog API service](../server/UnityCatalogServer.md) to handle HTTP requests at [/api/2.1/unity-catalog/iceberg](../server/UnityCatalogServer.md#addServices) URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/v1/config` | [config](#config) | `warehouse`
 GET | `/v1/catalogs/[catalog]/namespaces` | `listNamespaces` | `catalog`<br>`parent`<br>`pageToken`<br>`pageSize`
 HEAD | `/v1/catalogs/[catalog]/namespaces/[namespace]` | `namespaceExists` | `catalog`<br>`namespace`
 GET | `/v1/catalogs/[catalog]/namespaces/[namespace]` | `getNamespace` | `catalog`<br>`namespace`
 POST | `/v1/catalogs/[catalog]/namespaces` | `createNamespace` | `catalog`
 DELETE | `/v1/catalogs/[catalog]/namespaces/[namespace]` | `dropNamespace` | `catalog`<br>`namespace`
 POST | `/v1/catalogs/[catalog]/namespaces/[namespace]/properties` | `updateNamespaceProperties` | `catalog`<br>`namespace`
 GET | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables` | `listTables` | `catalog`<br>`namespace`<br>`pageToken`<br>`pageSize`
 POST | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables` | `createTable` | `catalog`<br>`namespace`
 HEAD | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]` | `tableExists` | `catalog`<br>`namespace`<br>`table`
 GET | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]` | [loadTable](#loadTable) | `catalog`<br>`namespace`<br>`table`
 POST | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]` | `updateTable` | `catalog`<br>`namespace`<br>`table`
 DELETE | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]` | `dropTable` | `catalog`<br>`namespace`<br>`table`<br>`purgeRequested`
 GET | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]/credentials` | `loadCredentials` | `catalog`<br>`namespace`<br>`table`
 POST | `/v1/catalogs/[catalog]/namespaces/[namespace]/tables/[table]/metrics` | `reportMetrics` | `catalog`<br>`namespace`<br>`table`
 POST | `/v1/catalogs/[catalog]/tables/rename` | `renameTable` | `catalog`
 GET | `/v1/catalogs/[catalog]/namespaces/[namespace]/views/[view]` | `loadView` | `catalog`<br>`namespace`<br>`view`

!!! note "server.iceberg-table.enabled"
    `createNamespace`, `dropNamespace`, `updateNamespaceProperties`, `createTable`, `updateTable`, `dropTable` and `renameTable` fail with an `INVALID_ARGUMENT` error when [server.iceberg-table.enabled](index.md#server.iceberg-table.enabled) is disabled.

`IcebergRestCatalogService` uses [Hibernate](#sessionFactory).

## Create Instance

`IcebergRestCatalogService` takes the following to be created:

* [CatalogService](#catalogService)
* <span id="schemaService"> [SchemaService](../server/SchemaService.md)
* <span id="tableService"> [TableService](../server/TableService.md)
* <span id="tableConfigService"> [TableConfigService](../iceberg/TableConfigService.md)
* [MetadataService](#metadataService)

`IcebergRestCatalogService` is created when:

* `UnityCatalogServer` is requested to [add the API services](../server/UnityCatalogServer.md#addServices)

### MetadataService { #metadataService }

`IcebergRestCatalogService` is given a [MetadataService](MetadataService.md) when [created](#create-instance).

This `MetadataService` is used to [load an iceberg table](#loadTable).

### CatalogService { #catalogService }

`IcebergRestCatalogService` is given a [CatalogService](../server/CatalogService.md) when [created](#create-instance).

This `CatalogService` is used for the following:

* [listNamespaces](#listNamespaces) with no parent
* [getNamespace](#getNamespace) with the catalog only (the first layer of Unity Catalog's three-level namespace)

### SessionFactory { #sessionFactory }

`IcebergRestCatalogService` [creates a SessionFactory](../persistent-storage/HibernateUtil.md#getSessionFactory) when [created](#creating-instance).

This `SessionFactory` is used for the following:

* [tableExists](#tableExists)
* [loadTable](#loadTable)
* [listTables](#listTables)

## Config { #config }

```java
ConfigResponse config(
  Optional<String> catalogOpt)
```

`config` expects the `warehouse` query parameter (the name of a catalog) and fails with a `BadRequestException` when it is not given.

`config` requests the catalog repository to look up the catalog (so a non-existent catalog is a `404`).

`config` responds with the following:

* `prefix` override set to `catalogs/[catalog]`
* The REST endpoints this server supports:
    * Read endpoints only when [server.iceberg-table.enabled](index.md#server.iceberg-table.enabled) is disabled
    * Read and write endpoints otherwise

## Load Table { #loadTable }

```java
LoadTableResponse loadTable(
  String namespace,
  String table)
```

`loadTable` expects the given `namespace` to be two-part and splits it into catalog and schema parts (using `.` as the separator).

`loadTable` requests the [TableRepository](#tableRepository) to [get the table metadata](../persistent-storage/TableRepository.md#getTable) (by the given `namespace` and `table` separated using `.`).

`loadTable` requests the [TableRepository](#tableRepository) for the [uniform metadata location](../persistent-storage/TableRepository.md#getTableUniformMetadataLocation) (by the catalog, schema and the given `table`).

`loadTable` requests the [MetadataService](#metadataService) for the [TableMetadata](MetadataService.md#readTableMetadata) for the uniform metadata location.

In the end, `loadTable` responds with the `TableMetadata`.
