# UserCli

`UserCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `user` sub-commands](#handle).

```console
$ ./bin/uc user --help
Please provide a valid sub-command for user.
Valid sub-commands for user are: get, create, update, list, delete
For detailed help on user sub-commands, use bin/uc user <sub-command> --help
```

## Handle Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

`handle` creates a `UsersApi` (with the given [ApiClient](../client/ApiClient.md)).

Subcommand | Handler | API Handlers
-|-|-
 `create` | [createUser](#createUser) | `UsersApi`
 `delete` | [deleteUser](#deleteUser) | `UsersApi`
 `get` | [getUser](#getUser) | `UsersApi`
 `list` | [listUsers](#listUsers) | `UsersApi`
 `update` | [updateUser](#updateUser) | `UsersApi`

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `user` command
