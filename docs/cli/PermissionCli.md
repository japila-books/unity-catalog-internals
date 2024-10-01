# PermissionCli

`PermissionCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `permission` sub-commands](#handle).

```console
$ ./bin/uc permission --help
Please provide a valid sub-command for permission.
Valid sub-commands for permission are: get, create, delete
For detailed help on permission sub-commands, use bin/uc permission <sub-command> --help
```

!!! note
    **Permissions** and **Privilege Assignments** are synonyms.

## Securable Types

There are the following types of the securables in Unity Catalog:

1. `catalog`
1. `function`
1. `metastore`
1. `registered_model`
1. `schema`
1. `table`
1. `volume`

## Handle Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

`handle` creates a `GrantsApi` (with the given [ApiClient](../client/ApiClient.md)).

Subcommand | Handler | API Handlers
-|-|-
 `create` | [updatePermission](#updatePermission) | `GrantsApi`
 `delete` | [updatePermission](#updatePermission) | `GrantsApi`
 `get` | [getPermission](#getPermission) | `GrantsApi`

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `permission` command

## Get Permission { #getPermission }

```java
String getPermission(
  GrantsApi grantsApi,
  JSONObject json)
```

`getPermission` handles `get` sub-command.

=== "Help"

    ``` bash
    ./bin/uc permission get --help
    ```

``` text
Usage: bin/uc permission get [options]
Required Params:
  --securable_type The type of the securable
  --name The name of the entity.
Optional Params:
  --server UC Server to connect to. Default is reference server.
  --auth_token PAT token to authorize uc requests.
  --output To indicate CLI output format preference. Supported values are json and jsonPretty.
  --principal The target principal of the permission change
```

---

`getPermission` extracts the following command-line options from the given `JSONObject`:

* `securable_type`
* `name`
* `principal`

`getPermission` requests the `GrantsApi` for the privilege assignments of the given `name` (of `securable_type` type).
