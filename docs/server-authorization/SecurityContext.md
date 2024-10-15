# SecurityContext

`SecurityContext` is used by [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext) to create the following:

* [AuthService](../server/AuthService.md#securityContext)
* [AuthDecorator](AuthDecorator.md#securityContext)

## Creating Instance

`SecurityContext` takes the following to be created:

* [Configuration directory](#configurationFolder)
* [SecurityConfiguration](#securityConfiguration)
* <span id="serviceName"> Service Name
* <span id="localIssuer"> Local Issuer

`SecurityContext` is created alongside [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext).

### Configuration Directory { #configurationFolder }

`SecurityContext` is given the path of a configuration directory when [created](#creating-instance).

The configuration directory is supposed to contain the following files:

* [certs.json](#certsFile)
* [token.txt](#serviceTokenFile)

!!! note "UnityCatalogServer"
    [UnityCatalogServer](../server/UnityCatalogServer.md#securityContext) uses `etc/conf` as the configuration directory.

### SecurityConfiguration { #securityConfiguration }

`SecurityContext` is given a [SecurityConfiguration](SecurityConfiguration.md) when [created](#creating-instance).

`SecurityContext` uses the `SecurityConfiguration` to initialize the following properties:

Property | Value
-|-
 [rsaPublicKey](#rsaPublicKey) | [rsaPublicKey](SecurityConfiguration.md#rsaPublicKey)
 [rsaPrivateKey](#rsaPrivateKey) | [rsaPrivateKey](SecurityConfiguration.md#rsaPrivateKey)
 [algorithm](#algorithm) | [algorithmRSA](SecurityConfiguration.md#algorithmRSA)
 [keyId](#keyId) | [getKeyId](SecurityConfiguration.md#getKeyId)

### Initialization

`SecurityContext` [creates a service token](#createServiceToken) as follows:

Token Claim | Value
-|-
Subject (`sub`) | [Service Name](#serviceName)
Issuer (`iss`) | [Local Issuer](#localIssuer)
Issued At (`iat`) | Current time (in millis)
Key Id (`kid`) | [Key](SecurityConfiguration.md#getKeyId) of this [SecurityConfiguration](#securityConfiguration)
JWT Id (`jti`) | Random UUID
Type (`type`) | `SERVICE`
Subject (`sub`) | `admin`

`SecurityContext` [creates the internal certs file](#createInternalCertsFile).

`SecurityContext` [creates the service token file](#createServiceTokenFile).

In the end, `SecurityContext` prints out the following INFO message to the logs (with the content of [certs.json](#getInternalCertsFile)):

``` text
--- Internal Certs Configuration --
[certs.json]
```

## <span id="getInternalCertsFile"> certs.json { #certsFile }

`SecurityContext` uses `certs.json` in the [configuration directory](#configurationFolder) to be an [internal certs file](#createInternalCertsFile).

`certs.json` is used when:

* `JwksOperations` is requested to [loadJwkProvider](JwksOperations.md#loadJwkProvider) (for the `internal` issuer)

## <span id="serviceToken"><span id="createServiceToken"> token.txt { #serviceTokenFile }

`SecurityContext` creates `token.txt` (in the [configuration directory](#configurationFolder)) as the service token.

Token Claim | Value
-|-
Subject (`sub`) | [Service Name](#serviceName)
Issuer (`iss`) | [Local Issuer](#localIssuer)
Issued At (`iat`) | Current time (in millis)
Key Id (`kid`) | [getKeyId](SecurityConfiguration.md#getKeyId) of this [SecurityConfiguration](#securityConfiguration)
JWT Id (`jti`) | Random UUID
Type (`type`) | `SERVICE`
Subject (`sub`) | `admin`

!!! note
    The difference between this service token (`token.txt`) and [access tokens](#createAccessToken) to be created are as follows:

    Token Claim | Service Token | Access Tokens
    -|-|-
    Type (`type`) | `SERVICE` | `ACCESS`
    Subject (`sub`) | `admin` | The subject (based on a `DecodedJWT`)

## Create Access Token { #createAccessToken }

```java
String createAccessToken(
  DecodedJWT decodedJWT)
```

`createAccessToken` determines the subject based on the following claims in the given `DecodedJWT`:

* `email` (preferred)
* `sub`

`createAccessToken` creates an access token as follows:

Token Claim | Value
-|-
Subject (`sub`) | [Service Name](#serviceName)
Issuer (`iss`) | [Local Issuer](#localIssuer)
Issued At (`iat`) | Current time (in millis)
Key Id (`kid`) | [getKeyId](SecurityConfiguration.md#getKeyId) of this [SecurityConfiguration](#securityConfiguration)
JWT Id (`jti`) | Random UUID
Type (`type`) | `ACCESS`
Subject (`sub`) | The subject (based on the given `DecodedJWT`)

`SecurityContext` signs the service token with the [algorithm](SecurityConfiguration.md#algorithmRSA) (of this [SecurityConfiguration](#securityConfiguration)).

---

`createAccessToken` is used when:

* `AuthService` is requested to [grant a token](../server/AuthService.md#grantToken)

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.security.SecurityContext` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.SecurityContext.name = io.unitycatalog.server.security.SecurityContext
logger.SecurityContext.level = all
```

Refer to [Logging](../logging.md).
