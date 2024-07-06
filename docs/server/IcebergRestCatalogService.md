---
title: IcebergRestCatalogService
---

# IcebergRestCatalogService &mdash; Apache Iceberg REST APIs

`IcebergRestCatalogService` is a [Unity Catalog API service](UnityCatalogServer.md) to handle HTTP requests at [/api/2.1/unity-catalog/iceberg](UnityCatalogServer.md#addServices) URL.

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

## Creating Instance

`IcebergRestCatalogService` takes the following to be created:

* [CatalogService](#catalogService)
* <span id="schemaService"> [SchemaService](SchemaService.md)
* <span id="tableService"> [TableService](TableService.md)

`IcebergRestCatalogService` is created when:

* `UnityCatalogServer` is requested to [add the API services](UnityCatalogServer.md#addServices)

### CatalogService { #catalogService }

`IcebergRestCatalogService` is given a [CatalogService](CatalogService.md) when [created](#creating-instance).

This `CatalogService` is used for the following:

* [listNamespaces](#listNamespaces) with no parent
* [getNamespace](#getNamespace) with the catalog only (the first layer of Unity Catalog's three-level namespace)

### SessionFactory { #sessionFactory }

`IcebergRestCatalogService` [creates a SessionFactory](HibernateUtil.md#getSessionFactory) when [created](#creating-instance).

This `SessionFactory` is used for the following:

* [tableExists](#tableExists)
* [loadTable](#loadTable)
* [listTables](#listTables)
