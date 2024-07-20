---
title: IcebergRestCatalogService
---

# IcebergRestCatalogService &mdash; Apache Iceberg REST APIs

`IcebergRestCatalogService` is a [Unity Catalog API service](../server/UnityCatalogServer.md) to handle HTTP requests at [/api/2.1/unity-catalog/iceberg](../server/UnityCatalogServer.md#addServices) URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/v1/config` | [config](#config) | &nbsp;
 GET | `/v1/namespaces/[namespace]` | [getNamespace](#getNamespace) | `namespace`
 GET | `/v1/namespaces` | [listNamespaces](#listNamespaces) | `parent`
 GET | `/v1/namespaces/[namespace]/tables` | [listTables](#listTables) | `namespace`
 GET | `/v1/namespaces/[namespace]/tables/[table]` | [loadTable](#loadTable) | `namespace`<br>`table`
 POST | `/v1/namespaces/[namespace]/tables/[table]/metrics` | [reportMetrics](#reportMetrics) | `namespace`<br>`table`
 HEAD | `/v1/namespaces/[namespace]/tables/[table]` | [tableExists](#tableExists) | `namespace`<br>`table`

`IcebergRestCatalogService` uses [Hibernate](#sessionFactory).

## Create Instance

`IcebergRestCatalogService` takes the following to be created:

* [CatalogService](#catalogService)
* <span id="schemaService"> [SchemaService](../server/SchemaService.md)
* <span id="tableService"> [TableService](../server/TableService.md)
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
