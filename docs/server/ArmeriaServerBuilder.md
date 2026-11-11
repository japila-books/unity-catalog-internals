# ArmeriaServerBuilder

## Creating Instance

`ArmeriaServerBuilder` takes the following to be created:

* <span id="port"> Port (default: [8080](UnityCatalogServer.md#DEFAULT_PORT))
* <span id="basePath"> Base Path (default: [/api/2.1/unity-catalog/](UnityCatalogServer.md#BASE_PATH))
* <span id="controlPath"> Control Path (default: [/api/1.0/unity-control/](UnityCatalogServer.md#CONTROL_PATH))
* <span id="serverProperties"> [ServerProperties](ServerProperties.md)

`ArmeriaServerBuilder` is created when:

* `UnityCatalogServer` is requested to [initializeServer](UnityCatalogServer.md#initializeServer)

### authorizationEnabled { #authorizationEnabled }

`authorizationEnabled` is set to [isAuthorizationEnabled](ServerProperties.md#isAuthorizationEnabled) when `ArmeriaServerBuilder` is [created](#creating-instance).

`authorizationEnabled` is used when:

* `ArmeriaServerBuilder` is requested to [bodyConverter](#bodyConverter) (for `AuthorizationGateConverter`)
