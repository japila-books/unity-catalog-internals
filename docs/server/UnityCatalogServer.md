---
title: UnityCatalogServer
---

# UnityCatalogServer &mdash; Unity Catalog's Localhost Reference Server

`UnityCatalogServer` is Unity Catalog's **Localhost Reference Server**.

`UnityCatalogServer` can be started on command line to [handle REST API requests](#addServices) at the [port](#port).

```console
./bin/start-uc-server [-p|--port port]
```

`UnityCatalogServer` starts Armeria documentation service at http://localhost:8081/docs and the other [Unity Catalog API services](#addServices).

## Port

`UnityCatalogServer` takes a port number when [created](#creating-instance).

Unless specified on command-line using `-p,--port <arg>` option, `UnityCatalogServer` defaults to `8080` or the closest one available.

## Creating Instance

`UnityCatalogServer` takes the following to be created:

* [Port](#port)

While being created, `UnityCatalogServer` builds the [Server](#server):

1. Handle HTTP requests at the given [port](#port)
1. Bind the Armeria documentation service ([Armeria]({{ armeria.javadoc }}/com/linecorp/armeria/server/docs/DocService.html)) under `/docs` URL
1. [Register the API services](#addServices)

`UnityCatalogServer` is created when:

* `UnityCatalogServer` command-line utility is [started](#main)

### Server

`UnityCatalogServer` creates a `Server` ([Armeria]({{ armeria.javadoc }}/com/linecorp/armeria/server/Server.html)) when [created](#creating-instance).

## Register API Services { #addServices }

```java
void addServices(
  ServerBuilder sb)
```

`addServices` creates and registers Unity Catalog API services at the `/api/2.1/unity-catalog/` base path.

URL | Service
-|-
 `/` | Returns `Hello, Unity Catalog!` message
 `/api/1.0/unity-control/auth` |  [AuthService](AuthService.md)
 `/api/2.1/unity-catalog/catalogs` | [CatalogService](CatalogService.md)
 `/api/2.1/unity-catalog/functions` | [FunctionService](FunctionService.md)
 `/api/2.1/unity-catalog/iceberg` | [IcebergRestCatalogService](../iceberg/IcebergRestCatalogService.md)
 `/api/2.1/unity-catalog/models` | [ModelService](ModelService.md)
 `/api/2.1/unity-catalog/schemas` | [SchemaService](SchemaService.md)
 `/api/2.1/unity-catalog/tables` | [TableService](TableService.md)
 `/api/2.1/unity-catalog/temporary-table-credentials` | [TemporaryTableCredentialsService](TemporaryTableCredentialsService.md)
 `/api/2.1/unity-catalog/temporary-volume-credentials` | [TemporaryVolumeCredentialsService](TemporaryVolumeCredentialsService.md)
 `/api/2.1/unity-catalog/volumes` | [VolumeService](VolumeService.md)

## Launch UnityCatalogServer { #main }

```java
void main(
  String[] args)
```

`main` starts probing for the available port from `8081` or the first argument specified on command line.

`main` [creates a UnityCatalogServer](#creating-instance).

`main` requests the `UnityCatalogServer` to [print out the welcome ASCII art message](#printArt).

`main` requests the `UnityCatalogServer` to [start](#start).

`main`...FIXME
