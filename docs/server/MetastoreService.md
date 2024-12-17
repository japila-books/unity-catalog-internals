# MetastoreService

`MetastoreService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) registers to handle HTTP requests to the base `/api/2.1/unity-catalog/` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/metastore_summary` | [getMetastoreSummary](#getMetastoreSummary) | &nbsp;

```console
$ http http://localhost:8080/api/2.1/unity-catalog/metastore_summary | jq '.metastore_id'
"92418bf6-e62c-4d4c-bb5d-e5eda5c82688"
```

## MetastoreRepository { #METASTORE_REPOSITORY }

`MetastoreService` requests the system-wide [MetastoreRepository](../persistent-storage/MetastoreRepository.md) when created.

This `MetastoreRepository` is used to [getMetastoreSummary](../persistent-storage/MetastoreRepository.md#getMetastoreSummary) to handle `GET /metastore_summary` requests.

## Get Metastore Summary { #getMetastoreSummary }

```java
HttpResponse getMetastoreSummary()
```

`getMetastoreSummary` requests the system-wide [MetastoreRepository](#METASTORE_REPOSITORY) instance for the [metastore summary](../persistent-storage/MetastoreRepository.md#getMetastoreSummary).
