# UnityCatalogCli

`UnityCatalogCli` can be [launched](#main) on command line using `./bin/uc` command-line utility.

## Options

### auth_token { #auth_token }

Personal access token (PAT) to authorize requests

When specified, `UnityCatalogCli` [creates an ApiClient](#getApiClient) (and a [ControlClient](#getControlClient)) that adds the bearer token in the HTTP `Authorization` header to every request.

```text
Authorization: Bearer [auth_token]
```

### server

Default: `http://localhost:8080`

## Launching Standalone Application { #main }

`main` [creates an ApiClient](#getApiClient) and handles the command (specified as the first argument on command line).

Command | Handler
-|-
 `auth` | [AuthCli](AuthCli.md)
 `catalog` | [CatalogCli](CatalogCli.md)
 `function` | [FunctionCli](FunctionCli.md)
 `metastore` | [MetastoreCli](MetastoreCli.md)
 `model_version` | [ModelVersionCli](ModelVersionCli.md)
 `permission` | [PermissionCli](PermissionCli.md)
 `registered_model` | [ModelCli](ModelCli.md)
 `schema` | [SchemaCli](SchemaCli.md)
 `table` | [TableCli](TableCli.md)
 `user` | [UserCli](UserCli.md)
 `volume` | [VolumeCli](VolumeCli.md)

## Creating ApiClient { #getApiClient }

```java
ApiClient getApiClient(
  CommandLine cmd)
```

`getApiClient` creates an [ApiClient](../client/ApiClient.md) with the following:

Attribute | Value
-|-
 The host name of the UC service | [server](#server) option
 The port number of the UC service | The port from the [server](#server) option, if specified, or one of the following: <ul><li>`443` for `https` scheme<li>`8080` for `http` scheme</ul>

## Logging

`UnityCatalogCli` uses `etc/conf/cli.log4j2.properties` as the logging configuration file (via [log4j.configurationFile]({{ log4j.manual }}/configuration.html#system-properties) configuration property).
