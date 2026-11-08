---
title: Iceberg Support
subtitle: Apache Iceberg REST Catalog in Unity Catalog Server
---

# Iceberg Support

Unity Catalog Server exposes [Apache Iceberg]({{ iceberg.home }}) tables through the Iceberg REST catalog APIs of [IcebergRestCatalogService](IcebergRestCatalogService.md).

??? note
    The initial support for loading Iceberg tables located in local paths and S3 was added through [this commit]({{ uc.commit }}/209895f0409a8bf87f6a7fa0de30d1868d6d6727).

## server.iceberg-table.enabled { #server.iceberg-table.enabled }

`server.iceberg-table.enabled` configuration property (in `etc/conf/server.properties`) controls whether Unity Catalog Server accepts changes to Apache Iceberg tables through [IcebergRestCatalogService](IcebergRestCatalogService.md).

Property | Value
-|-
 Default | `true`
 Valid values | `true` or `false` (case-insensitive)

With the property enabled (default), any engine that supports the Apache Iceberg REST protocol can create, write to, rename and drop Iceberg tables (and manage namespaces) in Unity Catalog Server.

With the property disabled, the Iceberg REST API turns read-only. Existing Iceberg tables stay readable, but the following operations are rejected:

* `createNamespace`, `updateNamespaceProperties` and `dropNamespace`
* `createTable`, `updateTable` (commits), `renameTable` and `dropTable`

`IcebergRestCatalogService` checks the property (using `ServerProperties.checkIcebergTableEnabled`) before it handles any of these requests and fails with an `INVALID_ARGUMENT` error:

```text
Iceberg table writes are currently disabled. To enable them, set 'server.iceberg-table.enabled=true' in server.properties
```

!!! note "Endpoints Advertised to Iceberg Clients"
    The [config](IcebergRestCatalogService.md#config) endpoint lists only the read endpoints when the property is disabled.
    Iceberg clients that honor the advertised endpoints do not even try to write.

`ServerProperties` validates the property when [created](../server/ServerProperties.md#creating-instance), so a value other than `true` or `false` fails the server startup.

## Demo

[Demo: Full Apache Iceberg Table Support](../demo/full-apache-iceberg-table-support.md)
