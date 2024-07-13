# CreateTable

`CreateTable` represents a request to create a new table instance (coming from [TableCli](../cli/TableCli.md#createTable)).

`CreateTable` is `POST`ed to `/tables` API endpoint of the [TableService](TableService.md#createTable) (to persist using [TableRepository](../persistent-storage/TableRepository.md#createTable)).

Property | Required | Description
-|-|-
 `catalog_name` | ✅ | Name of parent catalog
 `columns` | ✅ | An array of `ColumnInfo`s of the table's columns
 `comment` | | User-provided free-form text description
 `data_source_format` | ✅ | Data source format:<ul><li>`DELTA`<li>`CSV`<li>`JSON`<li>`AVRO`<li>`PARQUET`<li>`ORC`<li>`TEXT`</ul>
 `name` | ✅ | Name of table, relative to parent schema.
 `properties` | ✅ | Name of table, relative to parent schema.
 `schema_name` | ✅ | Name of parent schema relative to its parent catalog
 `storage_location` | | Storage root URL<br>⛔️ Required for `EXTERNAL` tables
 `table_type` | ✅ | One of the following:<ul><li>`MANAGED` ([not supported by the Localhost Reference Server](../persistent-storage/TableRepository.md#createTable))<li>`EXTERNAL`</ul>

??? note "OpenAPI Generator"
    `CreateTable` was auto-generated using [OpenAPI Generator]({{ openapi.home }}) based on Unity Catalog's [OpenAPI specification]({{ uc.github }}/api/all.yaml).

    [sbt-openapi-generator]({{ openapi.github }}/sbt-openapi-generator) 7.5.0 is used in the `client` sbt module of the `unitycatalog` project.
