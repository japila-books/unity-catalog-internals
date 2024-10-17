# Server Authorization

**Server Authorization** can be enabled in [Unity Catalog Server](../server/index.md) using [server.authorization](#server.authorization) property in `etc/conf/server.properties` configuration file.

## server.authorization { #server.authorization }

To enable the server authorization `server.authorization` property should be `enable` (case-insensitive).

With server authorization enabled, Unity Catalog Server registers [AuthDecorator](AuthDecorator.md) to intercept all requests to `/api/2.1/unity-catalog/`-prefixed URLs.

With server authorization enabled, Unity Catalog Server uses [JCasbinAuthorizer](JCasbinAuthorizer.md) for role-based access control (RBAC).

## UnityAccessDecorator

Unity Catalog Server uses [UnityAccessDecorator](UnityAccessDecorator.md) to enforce Role-Based Access Control (RBAC).

## Bearer Authentication

From [OpenAPI Guide](https://swagger.io/docs/specification/authentication/bearer-authentication/) (extra spacing mine):

> **Bearer Authentication** (_token authentication_) is an [HTTP authentication scheme](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) that involves security tokens called bearer tokens.
>
> The name "Bearer authentication" can be understood as "give access to the bearer of this token."
>
> The bearer token is a cryptic string, usually generated by the server in response to a login request.
>
> The client must send this token in the Authorization header when making requests to protected resources:
>
> ```text
> Authorization: Bearer <token>
> ```
>
> The Bearer authentication scheme was originally created as part of [OAuth 2.0](https://swagger.io/docs/specification/authentication/oauth2/) in [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750).
>
> Bearer authentication should only be used over HTTPS (SSL).

## Demo

### Enable Server Authorization

Add the following to `etc/conf/server.properties`:

```text
server.authorization=enable
```

!!! tip
    Enable `ALL` logging level for the following loggers:
	
	* [AuthDecorator](AuthDecorator.md#logging)
  	* [UnityAccessDecorator](UnityAccessDecorator.md#logging)

Start [Unity Catalog server](../server/index.md).

### Unauthorized Access

```console
❯ ./bin/uc catalog list
Exception in thread "main" java.lang.RuntimeException: io.unitycatalog.client.ApiException: listCatalogs call failed with: 401 - {"error_code":"UNAUTHENTICATED","details":[{"reason":"UNAUTHENTICATED","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"No authorization found."}
	at io.unitycatalog.cli.UnityCatalogCli.main(UnityCatalogCli.java:168)
Caused by: io.unitycatalog.client.ApiException: listCatalogs call failed with: 401 - {"error_code":"UNAUTHENTICATED","details":[{"reason":"UNAUTHENTICATED","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"No authorization found."}
	at io.unitycatalog.client.api.CatalogsApi.getApiException(CatalogsApi.java:77)
	at io.unitycatalog.client.api.CatalogsApi.listCatalogsWithHttpInfo(CatalogsApi.java:356)
	at io.unitycatalog.client.api.CatalogsApi.listCatalogs(CatalogsApi.java:333)
	at io.unitycatalog.cli.CatalogCli.listCatalogs(CatalogCli.java:74)
	at io.unitycatalog.cli.CatalogCli.handle(CatalogCli.java:39)
	at io.unitycatalog.cli.UnityCatalogCli.main(UnityCatalogCli.java:127)
```

### Authorized Access

Use `subject_token` as specified in `etc/conf/token.txt`.

```console
./bin/uc --auth_token $(cat etc/conf/token.txt) catalog list
```

```text
┌─────┬────────────┬──────────┬─────────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│ CREATED_AT  │UPDATED_AT│                 ID                 │
├─────┼────────────┼──────────┼─────────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │1721234405334│null      │f029b870-9468-4f10-badc-630b41e5690d│
└─────┴────────────┴──────────┴─────────────┴──────────┴────────────────────────────────────┘
```

You should see the following DEBUG messages in the server logs:

```text
DEBUG io.unitycatalog.server.service.AuthDecorator:47 - AuthDecorator checking /api/2.1/unity-catalog/catalogs?max_results=100
DEBUG io.unitycatalog.server.service.AuthDecorator:72 - Validating access-token for issuer: internal
DEBUG io.unitycatalog.server.service.AuthDecorator:92 - Access allowed for subject: "admin"
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:74 - AccessDecorator checking /api/2.1/unity-catalog/catalogs?max_results=100
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:252 - serviceName = io.unitycatalog.server.service.CatalogService, methodName = listCatalogs
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:194 - authorize expression = #defer
WARN  io.unitycatalog.server.auth.decorator.UnityAccessDecorator:89 - No authorization resource(s) found.
INFO  org.casbin.jcasbin:113 - Request: [655136aa-a802-471c-994e-a478eedfce0b, ca7a1095-537c-4f9c-a136-5ca1ab1ec0de, OWNER] ---> true
INFO  org.casbin.jcasbin:115 - Hit Policy: [655136aa-a802-471c-994e-a478eedfce0b, ca7a1095-537c-4f9c-a136-5ca1ab1ec0de, OWNER]
```