# UCProxy

`UCProxy` is a`TableCatalog` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/TableCatalog/)).

## TablesApi { #tablesApi }

`UCProxy` creates a `TablesApi` client when requested to [initialize](#initialize).

## Initialize TableCatalog { #initialize }

??? note "CatalogPlugin"

    ```scala
    initialize(
      name: String,
      options: CaseInsensitiveStringMap): Unit
    ```

    `initialize` is part of the `CatalogPlugin` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/CatalogPlugin#initialize)) abstraction.

`initialize` asserts that `uri` option is specified.

`initialize` creates an [ApiClient](../client/ApiClient.md) based on the `uri` option (the host, the port and the scheme).

`initialize` tells the `ApiClient` to use `Authorization` header for every request based on `token` option, if defined.

In the end, `initialize` creates this [TablesApi](#tablesApi).
