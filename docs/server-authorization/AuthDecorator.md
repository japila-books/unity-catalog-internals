# AuthDecorator

`AuthDecorator` is a `DecoratingHttpServiceFunction` ([Armeria]({{ armeria.api }}/com/linecorp/armeria/server/DecoratingHttpServiceFunction.html)) for a JWT access-token authorization in the [Unity Catalog Server](../server/index.md).

## Decoded JSON Web Token { #DECODED_JWT_ATTR }

```java
AttributeKey<DecodedJWT> DECODED_JWT_ATTR
```

`DECODED_JWT_ATTR` is an `AttributeKey` (Netty) with a JSON Web Token (decoded from its string representation).

`AuthDecorator` sets the decoded JSON Web Token while [serving incoming requests](#serve).

`DECODED_JWT_ATTR` is used when:

* [Scim2UserService](../server/Scim2UserService.md) is requested for the [current user](../server/Scim2UserService.md#getCurrentUser)
* `IdentityUtils` is requested for the [email address of the principal](IdentityUtils.md#findPrincipalEmailAddress)

## Serve Incoming HttpRequest { #serve }

??? note "DecoratingHttpServiceFunction"

    ```java
    HttpResponse serve(
      HttpService delegate,
      ServiceRequestContext ctx,
      HttpRequest req)
    ```

    `serve` is part of the `DecoratingHttpServiceFunction` ([Armeria]({{ armeria.api }}/com/linecorp/armeria/server/DecoratingHttpServiceFunction.html#serve(com.linecorp.armeria.server.HttpService,com.linecorp.armeria.server.ServiceRequestContext,com.linecorp.armeria.common.HttpRequest))) abstraction.

`serve` prints out the following DEBUG message to the logs (with the path of the given `HttpRequest`):

```text
AuthDecorator checking [path]
```

`serve` finds `Authorization` header in the given `HttpRequest`.

??? note "AuthorizationException"
    `serve` reports an `AuthorizationException` unless there is an `Authorization` header in the `HttpRequest`:

    ```text
    No authorization found.
    ```

`serve` makes sure that the `Authorization` header is `Bearer` with a JSON Web Token.

??? note "AuthorizationException"
    `serve` reports an `AuthorizationException` unless there is a `Bearer` token in the `HttpRequest`:

    ```text
    No Bearer found.
    ```

`serve` gets the issuer (the `iss` claim) and the keyId (the `kid` header claim) in the token.

`serve` prints out the following DEBUG message to the logs:

```text
Validating access-token for issuer: [issuer]
```

??? note "AuthorizationException"
    `serve` reports an `AuthorizationException` unless the access token is for `internal` issuer:

    ```text
    Invalid access token.
    ```

`serve` verifies the access token with the [verifier](JwksOperations.md#verifierForIssuerAndKey) for the issuer and the keyId.

`serve` prints out the following DEBUG message to the logs (with the `sub` claim of the access token):

```text
Access allowed for subject: [sub]
```

In the end, `serve` sets [DECODED_JWT_ATTR](#DECODED_JWT_ATTR) attribute in the `ServiceRequestContext`.

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.service.AuthDecorator` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.AuthDecorator.name = io.unitycatalog.server.service.AuthDecorator
logger.AuthDecorator.level = all
```

Refer to [Logging](../logging.md).
