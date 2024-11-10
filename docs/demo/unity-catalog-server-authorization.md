---
hide:
- navigation
---

# Demo: Unity Catalog Server Authorization

This demo shows how [Server Authorization](../server-authorization/index.md) works in Unity Catalog.

## Enable Server Authorization

Add the following to `etc/conf/server.properties`:

```text
server.authorization=enable
```

## Enable Authorization Logging

Enable `ALL` logging level for the following loggers:

* [AuthDecorator](../server-authorization/AuthDecorator.md#logging)
* [UnityAccessDecorator](../server-authorization/UnityAccessDecorator.md#logging)

## Start UC Server

Start [Unity Catalog server](../server/index.md).

```bash
./bin/start-uc-server
```

## Unauthorized Access

The UC server requires all interactions to be authenticated using a token or a cookie.

This is why you face "No authorization found." error message unless either is provided.

```bash
./bin/uc catalog list
```

```text
Exception in thread "main" java.lang.RuntimeException: io.unitycatalog.client.ApiException: listCatalogs call failed with: 401 - {"error_code":"UNAUTHENTICATED","details":[{"reason":"UNAUTHENTICATED","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"No authorization found."}
	at io.unitycatalog.cli.UnityCatalogCli.main(UnityCatalogCli.java:171)
Caused by: io.unitycatalog.client.ApiException: listCatalogs call failed with: 401 - {"error_code":"UNAUTHENTICATED","details":[{"reason":"UNAUTHENTICATED","metadata":{},"@type":"google.rpc.ErrorInfo"}],"stack_trace":null,"message":"No authorization found."}
	at io.unitycatalog.client.api.CatalogsApi.getApiException(CatalogsApi.java:77)
	at io.unitycatalog.client.api.CatalogsApi.listCatalogsWithHttpInfo(CatalogsApi.java:356)
	at io.unitycatalog.client.api.CatalogsApi.listCatalogs(CatalogsApi.java:333)
	at io.unitycatalog.cli.CatalogCli.listCatalogs(CatalogCli.java:78)
	at io.unitycatalog.cli.CatalogCli.handle(CatalogCli.java:39)
	at io.unitycatalog.cli.UnityCatalogCli.main(UnityCatalogCli.java:127)
```

## Authorized Access

Use the admin token that Unity Catalog uses internally and is conveniently stored in `etc/conf/token.txt`.

```bash
./bin/uc --auth_token $(cat etc/conf/token.txt) catalog list
```

```text
┌─────┬────────────┬──────────┬─────┬─────────────┬──────────┬──────────┬──────────┬────────────────────────────────────┐
│NAME │  COMMENT   │PROPERTIES│OWNER│ CREATED_AT  │CREATED_BY│UPDATED_AT│UPDATED_BY│                 ID                 │
├─────┼────────────┼──────────┼─────┼─────────────┼──────────┼──────────┼──────────┼────────────────────────────────────┤
│unity│Main catalog│{}        │null │1721234405334│null      │null      │null      │f029b870-9468-4f10-badc-630b41e5690d│
└─────┴────────────┴──────────┴─────┴─────────────┴──────────┴──────────┴──────────┴────────────────────────────────────┘
```

You should see the following DEBUG messages in the server logs:

```text
DEBUG io.unitycatalog.server.service.AuthDecorator:58 - AuthDecorator checking /api/2.1/unity-catalog/catalogs?max_results=100
DEBUG io.unitycatalog.server.service.AuthDecorator:74 - Validating access-token for issuer: internal and keyId: b995bc0a527ffbbf9b43f108a1a0d825a05eb4070b2831a88dfaf34d2e879733
DEBUG io.unitycatalog.server.service.AuthDecorator:93 - Access allowed for subject: "admin"
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:74 - AccessDecorator checking /api/2.1/unity-catalog/catalogs?max_results=100
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:252 - serviceName = io.unitycatalog.server.service.CatalogService, methodName = listCatalogs
DEBUG io.unitycatalog.server.auth.decorator.UnityAccessDecorator:194 - authorize expression = #deny
WARN  io.unitycatalog.server.auth.decorator.UnityAccessDecorator:89 - No authorization resource(s) found.
INFO  org.casbin.jcasbin:113 - Request: [cd941442-6635-45b9-bc7a-c9b527600b3b, 3c527572-1eb3-4e5e-ba95-fa136e1b6d62, OWNER] ---> true
INFO  org.casbin.jcasbin:115 - Hit Policy: [cd941442-6635-45b9-bc7a-c9b527600b3b, 3c527572-1eb3-4e5e-ba95-fa136e1b6d62, OWNER]
```
