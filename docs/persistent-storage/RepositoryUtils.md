# RepositoryUtils

## getSchemaId { #getSchemaId }

```java
UUID getSchemaId(
  Session session,
  String catalogName,
  String schemaName)
```

`getSchemaId` requests the system-wide [SchemaRepository](#SCHEMA_REPOSITORY) for the [SchemaInfoDAO](SchemaRepository.md#getSchemaDAO) for the given `catalogName` and `schemaName`.

??? note "BaseException"
    `getSchemaId` reports a `BaseException` when there is no schema found (by the given `catalogName` and `schemaName`).

    ```text
    Schema not found: [schemaName]"
    ```

In the end, `getSchemaId` returns the ID of the schema.

---

`getSchemaId` is used when:

* `ModelRepository` is requested to [findRegisteredModel](ModelRepository.md#findRegisteredModel), [createRegisteredModel](ModelRepository.md#createRegisteredModel), [listRegisteredModels](ModelRepository.md#listRegisteredModels), etc.
