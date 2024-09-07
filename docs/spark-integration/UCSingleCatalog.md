# UCSingleCatalog

`UCSingleCatalog` is a `TableCatalog` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/TableCatalog/)).

`UCSingleCatalog` supports [loading tables](#loadTable) from the following cloud object storages:

Cloud Object Storage | Scheme
-|-
 [Amazon S3](https://aws.amazon.com/s3/) | `s3://`
 [Google Cloud Storage](https://cloud.google.com/storage) | `gs://`

## DeltaCatalog { #deltaCatalog }

`UCSingleCatalog` creates a `DeltaCatalog` ([Delta Lake]({{ book.delta }}/DeltaCatalog)) when requested to [initialize](#initialize).

`DeltaCatalog` is a `DelegatingCatalogExtension` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/DelegatingCatalogExtension)) that is supposed to delegate to a [UCProxy](UCProxy.md).

## Initialize TableCatalog { #initialize }

??? note "CatalogPlugin"

    ```scala
    initialize(
      name: String,
      options: CaseInsensitiveStringMap): Unit
    ```

    `initialize` is part of the `CatalogPlugin` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/CatalogPlugin#initialize)) abstraction.

`initialize` creates a [UCProxy](UCProxy.md) to [initialize](UCProxy.md#initialize).

`initialize` creates a `DeltaCatalog` ([Delta Lake]({{ book.delta }}/DeltaCatalog)) that is told to delegate to the `UCProxy` for unsupported `TableCatalog` features.

!!! note "Dynamic Loading"
    `initialize` expects that `org.apache.spark.sql.delta.catalog.DeltaCatalog` class is available on the CLASSPATH only (not at build time) and loads it dynamically.
