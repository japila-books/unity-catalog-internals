# UCProxy

`UCProxy` is a`TableCatalog` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/TableCatalog/)).

## TablesApi { #tablesApi }

`UCProxy` creates a `TablesApi` client when requested to [initialize](#initialize).

## TemporaryTableCredentialsApi { #temporaryTableCredentialsApi }

`UCProxy` creates a `TemporaryTableCredentialsApi` client when requested to [initialize](#initialize).

## Initialize Table Catalog { #initialize }

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

In the end, `initialize` creates this [TablesApi](#tablesApi) and this [TemporaryTableCredentialsApi](#temporaryTableCredentialsApi).

## Load Table { #loadTable }

??? note "TableCatalog"

    ```java
    loadTable(
      ident: Identifier): Table
    ```

    `loadTable` is part of the `TableCatalog` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/TableCatalog#loadTable)) abstraction.

`loadTable` requests the [TablesApi](#tablesApi) to [load the metadata](../server/TableService.md#getTable) of the table by the fully-qualified table name (with the [name](#name) of this catalog):

```text
[catalog_name].[two-part ident (with the schema and table names)]
```

If the table metadata could be found, `loadTable` requests the [TemporaryTableCredentialsApi](#temporaryTableCredentialsApi) for the [S3 temporary table credentials](../server/TemporaryTableCredentialsService.md#generateTemporaryTableCredential) (sending a `POST` request to `/temporary-table-credentials` endpoint).

!!! note
    It is assumed that the temporary table credentials are for `READ_WRITE` operation.

For a table stored in a S3 bucket, `loadTable` sets the following Hadoop properties:

Hadoop Property | Value
-|-
 `fs.s3a.access.key` | `accessKeyId` of the `AwsCredentials`
 `fs.s3a.secret.key` | `secretAccessKey` of the `AwsCredentials`
 `fs.s3a.session.token` | `sessionToken` of the `AwsCredentials`
 `fs.s3a.impl` | `org.apache.hadoop.fs.s3a.S3AFileSystem`
 `fs.s3a.path.style.access` | `true`

`loadTable` creates a `CatalogTable` ([Spark SQL]({{ book.spark_sql }}/CatalogTable)) with the following:

* `MANAGED` and `EXTERNAL` tables are supported
* `locationUri` based on Unity Catalog's `storageLocation`

In the end, `loadTable` creates a `V1Table` ([Spark SQL]({{ book.spark_sql }}/connector/V1Table)) for the `CatalogTable`.

## List Namespaces { #listNamespaces }

??? note "SupportsNamespaces"

    ```scala
    listNamespaces(): Array[Array[String]]
    ```

    `listNamespaces` is part of the `SupportsNamespaces` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/SupportsNamespaces/#listNamespaces)) abstraction.

`listNamespaces`...FIXME

## List Tables { #listTables }

??? note "TableCatalog"

    ```scala
    listTables(
      namespace: Array[String]): Array[Identifier]
    ```

    `listTables` is part of the `TableCatalog` ([Spark SQL]({{ book.spark_sql }}/connector/catalog/TableCatalog/#listTables)) abstraction.

`listTables`...FIXME
