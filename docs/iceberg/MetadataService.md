# MetadataService

`MetadataService` is part of [IcebergRestCatalogService](IcebergRestCatalogService.md).

## Creating Instance

`MetadataService` takes the following to be created:

* [FileIOFactory](#fileIOFactory)

`MetadataService` is created when:

* `UnityCatalogServer` is requested to [register the API services](../server/UnityCatalogServer.md#addServices)

### FileIOFactory { #fileIOFactory }

`MetadataService` is given a [FileIOFactory](FileIOFactory.md) when [created]

## readTableMetadata { #readTableMetadata }

```java
TableMetadata readTableMetadata(
  String metadataLocation)
```

`readTableMetadata`...FIXME

---

`readTableMetadata` is used when:

* `IcebergRestCatalogService` is requested to [load an iceberg table](IcebergRestCatalogService.md#loadTable)
