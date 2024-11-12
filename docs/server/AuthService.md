# AuthService

`AuthService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle `/api/1.0/unity-control/auth` endpoint and perform [OAuth2 token exchange](#grantToken).

Method | URL | Handler | Params
-|-|-|-
 POST | `/tokens` | [grantToken](#grantToken) | `OAuthTokenExchangeRequest`

## Creating Instance

`AuthService` takes the following to be created:

* <span id="securityContext"> [SecurityContext](../server-authorization/SecurityContext.md)

Upon creation, `AuthService` creates the [JwksOperations](#jwksOperations).

`AuthService` is created when:

* `UnityCatalogServer` is requested to [register API services](UnityCatalogServer.md#addServices)

## Grant Token { #grantToken }

```java
HttpResponse grantToken(
  OAuthTokenExchangeRequest request)
```

`grantToken` prints out the following DEBUG message to the logs:

```text
Got token: [request]
```

??? note "OAuthInvalidRequestException"
    `grantToken` asserts the following or reports an `OAuthInvalidRequestException`:

    1. There must be `grant_type` specified as `urn:ietf:params:oauth:grant-type:token-exchange` grant type
    1. There must be `requested_token_type` specified as `urn:ietf:params:oauth:token-type:access_token` token type
    1. There must be `subject_token_type` specified
    1. There must be no `actor_token_type` specified (as not supported yet)

`grantToken` decodes the given `subject_token` JSON Web Token (JWT) (from the `OAuthTokenExchangeRequest`).

!!! note "No Verification of Token's Signature"
    `grantToken` performs no verification of the token's signature.

`grantToken` finds the issuer of the `subject_token` token, if specified (using `iss` claim).

`grantToken` finds the private claim (`keyId`) of the `subject_token` token, if specified (using `kid` header claim).

`grantToken` prints out the following DEBUG message to the logs:

```text
Validating token for issuer: [issuer]
```

`grantToken` requests the [JwksOperations](#jwksOperations) for the [verifier](../server-authorization/JwksOperations.md#verifierForIssuerAndKey) for the issuer and private claim.

`grantToken` uses the `JWTVerifier` to verify the decoded `subject_token` JSON Web Token.

`grantToken` prints out the following DEBUG message to the logs:

```text
Validated. Creating access token.
```

`grantToken` requests the [SecurityContext](#securityContext) to [create an access token](../server-authorization/SecurityContext.md#createAccessToken) for the decoded and verified `subject_token` JSON Web Token.

In the end, `grantToken` responds with the following:

Property | Value
-|-
 `accessToken` | The generated access token
 `issuedTokenType` | `urn:ietf:params:oauth:token-type:access_token`
 `tokenType` | `Bearer`

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.service.AuthService` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.AuthService.name = io.unitycatalog.server.service.AuthService
logger.AuthService.level = all
```

Refer to [Logging](../logging.md).
