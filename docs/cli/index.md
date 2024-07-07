# Unity Catalog CLI

**Unity Catalog CLI** can be started using `./bin/uc` command-line utility that runs [UnityCatalogCli](UnityCatalogCli.md).

```text
$ ./bin/uc --help

Usage: bin/uc <entity> <operation> [options]
Entities: schema, volume, catalog, function, table

By default, the client will connect to UC running locally at http://localhost:8080

To connect to specific UC server, use --server https://<host>

Currently, auth using bearer token is supported. Please specify the token via --auth_token <PAT Token>

For detailed help on entity specific operations, use bin/uc <entity> --help
```

## Entities

Unity Catalog CLI supports the following entities:

* [schema](SchemaCli.md)
* [volume](VolumeCli.md)
* [catalog](CatalogCli.md)
* [function](FunctionCli.md)
* [table](TableCli.md)

## Options

### <span id="OUTPUT"> output { #output }

The output format

Format | Description
-|-
 `json` | Prints out the output directly (with no changes) for `read` and `call` subcommands when [postProcessAndPrintOutput](CliUtils.md#postProcessAndPrintOutput)
 `jsonPretty` | Uses the default `PrettyPrinter` for the [ObjectWriter](CliUtils.md#getObjectWriter) to pretty-print JSONs
