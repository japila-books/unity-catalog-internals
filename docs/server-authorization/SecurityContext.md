# SecurityContext

`SecurityContext` is created alongside [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext).

## Creating Instance

`SecurityContext` takes the following to be created:

* <span id="configurationFolder"> [Configuration directory](#configurationFolder)
* <span id="securityConfiguration"> [SecurityConfiguration](SecurityConfiguration.md)
* <span id="serviceName"> Service Name
* <span id="localIssuer"> Local Issuer

`SecurityContext` is created alongside [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext).

### Configuration Directory { #configurationFolder }

`SecurityContext` is given the path of a configuration directory with the following files:

* [certs.json](#certsFile)
* [token.txt](#serviceTokenFile)

!!! note "UnityCatalogServer"
    [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext) uses `etc/conf` as the configuration directory.
