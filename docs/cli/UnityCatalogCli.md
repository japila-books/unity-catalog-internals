# UnityCatalogCli

`UnityCatalogCli` can be [launched](#main) on command line (using `./bin/uc` command-line utility).

## Options

### auth_token { #auth_token }

Personal access token (PAT) to authorize requests

When specified, `UnityCatalogCli` [creates an ApiClient](#getApiClient) that adds `Authorization` header with `Bearer [pat]` to every request.

## Logging

`UnityCatalogCli` uses `etc/conf/cli.log4j2.properties` as the logging configuration file (via [log4j.configurationFile]({{ log4j.manual }}/configuration.html#system-properties) configuration property).
