# Unity Catalog CLI

**Unity Catalog CLI** can be started using `./bin/uc` command-line utility that runs [UnityCatalogCli](UnityCatalogCli.md).

```text
$ ./bin/uc --help

Usage: bin/uc <entity> <operation> [options]
Entities: schema, volume, model_version, auth, catalog, function, registered_model, table

By default, the client will connect to UC running locally at http://localhost:8080

To connect to specific UC server, use --server https://<host>:<port>

Currently, auth using bearer token is supported. Please specify the token via --auth_token <PAT Token>

For detailed help on entity specific operations, use bin/uc <entity> --help
```

## Entities

Unity Catalog CLI supports the following entities (commands):

* [auth](AuthCli.md)
* [catalog](CatalogCli.md)
* [function](FunctionCli.md)
* [model_version](ModelVersionCli.md)
* [registered_model](ModelCli.md)
* [schema](SchemaCli.md)
* [table](TableCli.md)
* [volume](VolumeCli.md)

## Options

### <span id="OUTPUT"> output { #output }

The output format

Format | Description
-|-
 `json` | Prints out the output directly (with no changes) for `read` and `call` subcommands when [postProcessAndPrintOutput](CliUtils.md#postProcessAndPrintOutput)
 `jsonPretty` | Uses the default `PrettyPrinter` for the [ObjectWriter](CliUtils.md#getObjectWriter) to pretty-print JSONs

## Fixed-Width Output Fields

As of [this commit]({{ uc.commit }}/06ea446a3a00e78f82a77039dae22339152e2e1d), the tabular output of Unity Catalog CLI always displays the entire values of the following columns (case-insensitive):

* `NAME`
* Any column with `ID` suffix (e.g., `TABLE_ID`)

``` { .console .no-copy }
$ ./bin/uc table list --catalog unity --schema default
┌─────────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────────────────────────────┐
│      NAME       │CATALOG_NAME│SCHEMA_NAME │ TABLE_TYPE │DATA_SOURCE_│  COLUMNS   │STORAGE_LOCA│  COMMENT   │ PROPERTIES │ CREATED_AT │ UPDATED_AT │              TABLE_ID              │
│                 │            │            │            │   FORMAT   │            │    TION    │            │            │            │            │                                    │
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│numbers          │unity       │default     │EXTERNAL    │DELTA       │[{"name":...│file:///U...│External ...│{"key1":"...│172042953...│172042953...│b5d6db68-5eca-485c-be5f-5f53d4f27f60│
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│marksheet_uniform│unity       │default     │EXTERNAL    │DELTA       │[{"name":...│file:///t...│Uniform t...│{"key1":"...│172042953...│172042953...│76874c28-0ebf-46e7-9971-eb164bd62c46│
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│marksheet        │unity       │default     │MANAGED     │DELTA       │[{"name":...│file:///U...│Managed t...│{"key1":"...│172042953...│172042953...│25ca07aa-1350-4104-b485-13b9ad1f5d72│
└─────────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────────────────────────────┘
```

## Read-Write Support for Delta Tables Only

Only delta tables are supported for [read](TableCli.md#readTable) and [write](TableCli.md#writeTable) operations.
