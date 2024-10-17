# MetastoreCli

`MetastoreCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `metastore` sub-commands](#handle).

``` console
❯ ./bin/uc metastore --help
Please provide a valid sub-command for metastore.
Valid sub-commands for metastore are: get
For detailed help on metastore sub-commands, use bin/uc metastore <sub-command> --help
```

## Handle Command Line { #handle }

``` java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd` that can currently by `get` only.

`handle` creates a `MetastoresApi` (with the given [ApiClient](../client/ApiClient.md)).

Subcommand | Handler | API Handlers
-|-|-
 `get` | &nbsp; | `MetastoresApi`

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `metastore` command
