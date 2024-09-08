# SchemaRepository

## Find SchemaDAO by Catalog and Schema Names { #getSchemaDAO }

```java
SchemaInfoDAO getSchemaDAO(
  Session session,
  String catalogName,
  String schemaName)
```

`getSchemaDAO` requests the system-wide [CatalogRepository](#CATALOG_REPOSITORY) for the [CatalogInfoDAO](CatalogRepository.md#getCatalogDAO).

??? note "BaseException"
    `getSchemaId` reports a `BaseException` when the `catalogName` catalog could not be found.

    ```text
    Catalog not found: [catalogName]"
    ```

In the end, `getSchemaDAO` [finds the SchemaInfoDAO](#getSchemaDAO-catalogId) for the catalog and the `schemaName` schema.

---

`getSchemaDAO` is used when:

* `FunctionRepository` is requested to [createFunction](FunctionRepository.md#createFunction), [getSchemaId](FunctionRepository.md#getSchemaId), [getFunctionDAO](FunctionRepository.md#getFunctionDAO), [deleteFunction](FunctionRepository.md#deleteFunction)
* `SchemaRepository` is requested to [createSchema](#createSchema), [getSchemaDAO](#getSchemaDAO-fullName), [updateSchema](#updateSchema)
* `TableRepository` is requested to [getSchemaId](TableRepository.md#getSchemaId)
* `VolumeRepository` is requested to [createVolume](VolumeRepository.md#createVolume), [getVolumeDAO](VolumeRepository.md#getVolumeDAO), [listVolumes](VolumeRepository.md#listVolumes), [deleteVolume](VolumeRepository.md#deleteVolume)
* `RepositoryUtils` is requested to [getSchemaId](RepositoryUtils.md#getSchemaId)

## Find SchemaDAO by Catalog ID and Schema Name { #getSchemaDAO-catalogId }

```java
SchemaInfoDAO getSchemaDAO(
  Session session,
  UUID catalogId,
  String schemaName)
```

`getSchemaDAO` creates the following query (using the given `Session`) for the given `schemaName` and `catalogId`:

```text
FROM SchemaInfoDAO WHERE name = [schemaName] and catalogId = :catalogId
```

`getSchemaDAO` executes the query and returns a single result of the query, or `null` if the query returns no results.

---

`getSchemaDAO` is used when:

* `SchemaRepository` is requested to [delete a schema](#deleteSchema)
