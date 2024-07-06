# UnityCatalogCli

`UnityCatalogCli` can be [launched](#main) on command line using `./bin/uc` command-line utility.

## Options

### auth_token { #auth_token }

Personal access token (PAT) to authorize requests

When specified, `UnityCatalogCli` [creates an ApiClient](#getApiClient) that adds `Authorization` header with `Bearer [pat]` to every request.

### server

Default: `http://localhost:8080`

## Launching Standalone Application { #main }

`main` [creates an ApiClient](#getApiClient) and handles the command (specified as the first argument on command line).

Command | Handler
-|-
 `catalog` | [CatalogCli](CatalogCli.md#handle)
 `function` | [FunctionCli](FunctionCli.md#handle)
 `schema` | [SchemaCli](SchemaCli.md#handle)
 `table` | [TableCli](TableCli.md#handle)
 `volume` | [VolumeCli](VolumeCli.md#handle)

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
