# KeyMapperUtil

## Resolve Resource Names Into IDs { #mapResourceKeys }

``` java
Map<SecurableType, Object> mapResourceKeys(
  Map<SecurableType, Object> resourceKeys)
```

??? note "Static Method"
    `mapResourceKeys` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`mapResourceKeys` resolves the given `SecurableType`s with their names (`resourceKeys`) into `SecurableType`s with IDs (in the given order).

 Resource Keys | SecurableType | ID | Repository
-|-|-|-
 CATALOG, SCHEMA, TABLE | TABLE | `table_id` | [TableRepository](../persistent-storage/TableRepository.md#getTable)
 TABLE<br>(with neither CATALOG nor SCHEMA) | TABLE<br>SCHEMA<br>CATALOG | `table_id`<br>`schema_id`<br>`id` | [TableRepository](../persistent-storage/TableRepository.md#getTable)<br>[SchemaRepository](../persistent-storage/SchemaRepository.md#getSchema)<br>[CatalogRepository](../persistent-storage/CatalogRepository.md#getCatalog)
 CATALOG, SCHEMA, VOLUME | VOLUME | `volume_id` | [VolumeRepository](../persistent-storage/VolumeRepository.md#getVolume)
 VOLUME<br>(with neither CATALOG nor SCHEMA) | &nbsp; | &nbsp; | &nbsp;
 CATALOG, SCHEMA, FUNCTION | &nbsp; | &nbsp; | &nbsp;
 FUNCTION<br>(with neither CATALOG nor SCHEMA) | &nbsp; | &nbsp; | &nbsp;
 CATALOG, SCHEMA, REGISTERED_MODEL | &nbsp; | &nbsp; | &nbsp;
 REGISTERED_MODEL<br>(with neither CATALOG nor SCHEMA) | &nbsp; | &nbsp; | &nbsp;
 CATALOG, SCHEMA | SCHEMA | `schema_id` | [SchemaRepository](../persistent-storage/SchemaRepository.md#getSchema)
 SCHEMA<br>(with no CATALOG) | SCHEMA<br>CATALOG | `schema_id`<br>`id` | [SchemaRepository](../persistent-storage/SchemaRepository.md#getSchema)<br>[CatalogRepository](../persistent-storage/CatalogRepository.md#getCatalog)
 CATALOG | CATALOG | `id` | [CatalogRepository](../persistent-storage/CatalogRepository.md#getCatalog)
 METASTORE | METASTORE | `ca7a1095-537c-4f9c-a136-5ca1ab1ec0de` | [MetastoreRepository](../persistent-storage/MetastoreRepository.md#getMetastoreId)

---

`mapResourceKeys` is used when:

* `UnityAccessDecorator` is requested to [check authorization](UnityAccessDecorator.md#checkAuthorization)
* `TemporaryModelVersionCredentialsService` is requested to [authorizeForOperation](../server/TemporaryModelVersionCredentialsService.md#authorizeForOperation)
* `TemporaryTableCredentialsService` is requested to [authorizeForOperation](../server/TemporaryTableCredentialsService.md#authorizeForOperation)
* `TemporaryVolumeCredentialsService` is requested to [authorizeForOperation](../server/TemporaryVolumeCredentialsService.md#authorizeForOperation)
