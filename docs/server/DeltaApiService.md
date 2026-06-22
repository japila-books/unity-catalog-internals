---
title: DeltaApiService
subtitle: REST API for Delta Tables
---

# DeltaApiService &mdash; REST API for Delta Tables

`DeltaApiService` is a [Unity Catalog API service](UnityCatalogServer.md) to handle the [API endpoints](#ENDPOINTS) under [`/api/2.1/unity-catalog/`](UnityCatalogServer.md#addApiServices) path.

Method | URL | Handler | Params
-|-|-|-
 GET | `/delta/v1/config`| [getConfig](#getConfig) | <ul><li>catalog</li><li>protocolVersions</li></ul>
 GET | `/delta/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}`| [loadTable](#loadTable) | <ul><li>catalog</li><li>schema</li><li>table</li></ul>
 POST | `/delta/v1/catalogs/{catalog}/schemas/{schema}/staging-tables`| [createStagingTable](#createStagingTable) | <ul><li>catalog</li><li>schema</li></ul>
 POST | `/delta/v1/catalogs/{catalog}/schemas/{schema}/tables`| [createTable](#createTable) | <ul><li>catalog</li><li>schema</li></ul>
 POST | `/delta/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}`| [updateTable](#updateTable) | <ul><li>catalog</li><li>schema</li><li>table</li></ul>
 GET | `/delta/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/credentials`| [getTableCredentials](#getTableCredentials) | <ul><li>catalog</li><li>schema</li><li>table</li><li>operation</li></ul>
 GET | `/delta/v1/staging-tables/{table_id}/credentials`| [getStagingTableCredentials](#getStagingTableCredentials) | <ul><li>table_id</li></ul>

`DeltaApiService` is an [AuthorizedService](AuthorizedService.md).

## Creating Instance

`DeltaApiService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)
* <span id="repositories"> [Repositories](Repositories.md)
* <span id="serverProperties"> [ServerProperties](ServerProperties.md)
* <span id="storageCredentialVendor"> [StorageCredentialVendor](../credential-vending/StorageCredentialVendor.md)

While being created, `DeltaApiService` uses this [Repositories](#repositories) for the following repositories:

* <span id="catalogRepository"> [CatalogRepository](Repositories.md#getCatalogRepository)
* <span id="schemaRepository"> [SchemaRepository](Repositories.md#getSchemaRepository)
* <span id="tableRepository"> [TableRepository](Repositories.md#getTableRepository)
* <span id="stagingTableRepository"> [StagingTableRepository](Repositories.md#getStagingTableRepository)

`DeltaApiService` is created when:

* `UnityCatalogServer` is requested to [register the Unity Catalog API services](UnityCatalogServer.md#addDeltaApiServices)

## API Endpoints { #ENDPOINTS }

`DeltaApiService` supports the following API endpoints:

API Endpoint | HTTP Method
-|-
 `/v1/catalogs/{catalog}/schemas/{schema}/staging-tables` | POST
 `/v1/catalogs/{catalog}/schemas/{schema}/tables` | POST
 `/v1/catalogs/{catalog}/schemas/{schema}/tables` | GET
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}` | GET
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}` | POST
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}` | DELETE
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}` | HEAD
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/rename` | POST
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/credentials` | GET
 `/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/metrics` | POST
 `/v1/staging-tables/{table_id}/credentials` | GET
 `/v1/temporary-path-credentials` | GET

## Vend Temporary Storage Credentials for Table Operation { #getTableCredentials }

```java
DeltaCredentialsResponse getTableCredentials(
  String catalog,
  String schema,
  String table,
  DeltaCredentialOperation operation)
```

`getTableCredentials` requests the [TableRepository](#tableRepository) for the [storage location](../persistent-storage/TableRepository.md#getTableStorageLocation) of the table (given the three parts, `catalog`, `schema`, and `table`).

`getTableCredentials` requests the [StorageCredentialVendor](#storageCredentialVendor) for the [temporary credentials](../credential-vending/StorageCredentialVendor.md#vendCredential) to [execute the given `operation`](#toPrivileges) on the storage location.

---

`getTableCredentials` is used when:

* `DeltaApiService` is requested to handle GET requests on `/delta/v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/credentials` URL

### toPrivileges { #toPrivileges }

```java
Set<CredentialContext.Privilege> toPrivileges(
  DeltaCredentialOperation operation)
```

`toPrivileges`...FIXME

## Demo

``` bash
$ http http://localhost:8080/api/2.1/unity-catalog/catalogs \
    | jq '.catalogs[].name'
"unity"
```

```console
$ http http://localhost:8080/api/2.1/unity-catalog/delta/v1/config \
    catalog==unity \
    protocol-versions==1.0
HTTP/1.1 200 OK
content-length: 755
content-type: application/json; charset=utf-8
date: Mon, 22 Jun 2026 18:33:56 GMT
server: Armeria/1.28.4

{
    "endpoints": [
        "POST /v1/catalogs/{catalog}/schemas/{schema}/staging-tables",
        "POST /v1/catalogs/{catalog}/schemas/{schema}/tables",
        "GET /v1/catalogs/{catalog}/schemas/{schema}/tables",
        "GET /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}",
        "POST /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}",
        "DELETE /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}",
        "HEAD /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}",
        "POST /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/rename",
        "GET /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/credentials",
        "POST /v1/catalogs/{catalog}/schemas/{schema}/tables/{table}/metrics",
        "GET /v1/staging-tables/{table_id}/credentials",
        "GET /v1/temporary-path-credentials"
    ],
    "protocol-version": "1.0"
}
```
