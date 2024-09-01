# AuthService

`AuthService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle `/api/1.0/unity-control/auth` endpoint and perform [OAuth2 token exchange](#grantToken).

Method | URL | Handler | Params
-|-|-|-
 POST | `/tokens` | [grantToken](#grantToken) | `OAuthTokenExchangeRequest`

!!! note
    `AuthService` is the only API service registered under `/api/1.0/` URI.

## Demo

Use `subject_token` as specified in `etc/conf/token.txt`.

Use https://jwt.io/#encoded-jwt to work with JSON web tokens.

```bash
http --form http://localhost:8081/api/1.0/unity-control/auth/tokens \
    grant_type=urn:ietf:params:oauth:grant-type:token-exchange \
    requested_token_type=urn:ietf:params:oauth:token-type:access_token \
    subject_token_type=urn:ietf:params:oauth:token-type:id_token \
    subject_token=eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJhZG1pbiIsImlzcyI6ImludGVybmFsIiwiaWF0IjoxNzI1MTkxNzYzLCJqdGkiOiJmYThlNThiNS1lMzAyLTRlMmEtYWI4Zi0wZWNlNDI2MzA3OTMiLCJ0eXBlIjoiU0VSVklDRSJ9.RZAtSOe1YwXRzCKwgzmGxO6PQ28Ms7nBrKlbYGFKOXnZFlFsHu156ABjciINDhVZANg9oXQYsKBk9316tUs5hS5e4mKRHdBy-YXcN26nZIqrfhtNf6JAi8xCS4D6bgaOl1n_Nis1oDerl6IkqWSfz6Uj0-Z_zyGxt_Svkw199ClAvAG9rGkgVYV35-N8y4TTYy6IebA5r3S6LY6_NIVNg9vSjQd5oUQeDJ16-k4xcAlFZPYseNWtTKUdub427JGL0Z14q_dgX6gyAT6ibwOzfay3_97Dddi-bMm9kNH4Ahvvx167KRkPjTuazUaUc2sxlpVvLVGyCSYr3uUDjpVbSQ
```

```text
HTTP/1.1 200 OK
content-length: 734
content-type: application/json
date: Sun, 1 Sep 2024 20:03:35 GMT
server: Armeria/1.28.4

{
    "access_token": "eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJhZG1pbiIsImlzcyI6ImludGVybmFsIiwiaWF0IjoxNzI1MjIxMDE1LCJqdGkiOiJlNzJlODFhYi0xNDhkLTQ1ZjMtOTc2OS01Mjk5ODFhZjZlYTQiLCJ0eXBlIjoiQUNDRVNTIn0.Sn_BUz7I19W8eP2-A5iyomw4RW21E6MwpeItzjr-4QszwLMBuBCb8Dro6ICV1rqeI61Rax3NGaSR3HVxeB34gYXtXj74Wac3FbPY_6zWYBvzzfaLthafYI9qIMaUJmrJ98uRB1CV6be2PwfU34I9JPr2DxkmAhgMdofyi_JuasOmsTrtk7g12A0-tCjx8bAB39xeN3t0dOT68d-jO34eUa35YSl9g1WksxPP58Kqk5tOqXFtpHJaLOa-L16QnkKaXUGIran2SVYw7oApgoox-1bDOYEm2qy_j5Gz7ZmBbRIHGI3csuzXxaVUgBeHK8oi3YAQii0foYjQvbi6fg9egA",
    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "token_type": "Bearer"
}
```

```bash
http --form http://localhost:8081/api/1.0/unity-control/auth/tokens \
    grant_type=urn:ietf:params:oauth:grant-type:token-exchange \
    requested_token_type=urn:ietf:params:oauth:token-type:access_token \
    subject_token_type=urn:ietf:params:oauth:token-type:id_token \
    subject_token=eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJhZG1pbiIsImlzcyI6ImludGVybmFsIiwiaWF0IjoxNzI1MTkxNzYzLCJqdGkiOiJmYThlNThiNS1lMzAyLTRlMmEtYWI4Zi0wZWNlNDI2MzA3OTMiLCJ0eXBlIjoiU0VSVklDRSJ9.RZAtSOe1YwXRzCKwgzmGxO6PQ28Ms7nBrKlbYGFKOXnZFlFsHu156ABjciINDhVZANg9oXQYsKBk9316tUs5hS5e4mKRHdBy-YXcN26nZIqrfhtNf6JAi8xCS4D6bgaOl1n_Nis1oDerl6IkqWSfz6Uj0-Z_zyGxt_Svkw199ClAvAG9rGkgVYV35-N8y4TTYy6IebA5r3S6LY6_NIVNg9vSjQd5oUQeDJ16-k4xcAlFZPYseNWtTKUdub427JGL0Z14q_dgX6gyAT6ibwOzfay3_97Dddi-bMm9kNH4Ahvvx167KRkPjTuazUaUc2sxlpVvLVGyCSYr3uUDjpVbSQ | jq .access_token
```

```text
"eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJhZG1pbiIsImlzcyI6ImludGVybmFsIiwiaWF0IjoxNzI1MjIyNjIzLCJqdGkiOiJjMGE0ZTRiNC1mMGJjLTQ4ZDAtOTA3Ny01MzgyNWEzMWJjYzQiLCJ0eXBlIjoiQUNDRVNTIn0.fPyFNB3wcQ6tAoR-mnWGpoWtVwuvcEuSk43ZsYvNwOuddedWBeqH8TivR13GsC876jEzyPG4x1PtN2uOFHiNtfTXTZbEHUTlYoWlMU-BCZysuggUCih5fkbV63KdQkluLB1CyP3A-L4Dg6hxjbj-3V2jMoRjD5d_42k9yv1vuOe8sh1DNbaYXqBpnRNCdtD4IxJ6yRzBDLL6XcRlyombnj40AV7U5pxePz7PVlpfRix-GEEtnsA-wFxu3Ng-1lHBS9LEc0vmYUBe_P3ztNSon63al_CTStZz53S3moT-D0lsuDioYsnD7VNPHU31PhZVZ-rS-VAsFdQpHbiSeG1Fow"
```

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

`grantToken` uses the `JWTVerifier` to verify the decoded `subject_token` Json Web Token.

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
