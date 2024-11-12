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
* [AuthService](../server/AuthService.md#logging)
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

## Authorized Access (Admin User)

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

## Create User

Use the admin's token to create a new user (`demo@unitycatalog.io`).

```bash
bin/uc user create \
    --auth_token $(cat etc/conf/token.txt) \
    --name "Demo Unity Catalog" \
    --email "demo@unitycatalog.io"
```

```bash
bin/uc user create \
    --auth_token $(cat etc/conf/token.txt) \
    --name "Jacek Laskowski" \
    --email "jacek@japila.pl"
```

## List Users

```bash
./bin/uc user list --auth_token $(cat etc/conf/token.txt)
```

```text
┌────────────────────────────────────┬───────────────┬───────────────┬───────────┬───────┬───────────┬─────────────┬─────────────┐
│                 ID                 │     NAME      │     EMAIL     │EXTERNAL_ID│ STATE │PICTURE_URL│ CREATED_AT  │ UPDATED_AT  │
├────────────────────────────────────┼───────────────┼───────────────┼───────────┼───────┼───────────┼─────────────┼─────────────┤
│cd941442-6635-45b9-bc7a-c9b527600b3b│Admin          │admin          │null       │ENABLED│null       │1731087616216│1731244513779│
├────────────────────────────────────┼───────────────┼───────────────┼───────────┼───────┼───────────┼─────────────┼─────────────┤
│42613e87-487f-4b54-98af-ced544224328│Jacek Laskowski│jacek@japila.pl│null       │ENABLED│null       │1731242484262│1731244513779│
└────────────────────────────────────┴───────────────┴───────────────┴───────────┴───────┴───────────┴─────────────┴─────────────┘
```

## Generate Personal Access Token

Use [jwt.io](https://jwt.io) to generate a token.

!!! note "Issuer Claim"
    Unity Catalog server uses `etc/conf/certs.json` file to look up `kid` claim for the one and only `internal` issuer.

    ```console
    $ jq '.keys[].kid' etc/conf/certs.json
    "b995bc0a527ffbbf9b43f108a1a0d825a05eb4070b2831a88dfaf34d2e879733"
    ```

### Header

Use the following as the JWT token's header:

```json
{
  "kid": "b995bc0a527ffbbf9b43f108a1a0d825a05eb4070b2831a88dfaf34d2e879733",
  "alg": "RS512",
  "typ": "JWT"
}
```

### Payload

The `sub` claim is used as the user name. Use the following as the JWT token's payload.

```json
{
  "sub": "jacek@japila.pl",
  "iss": "internal"
}
```

### Verify Signature

!!! warning
    The following public and private keys are included in the source code of Unity Catalog.

In Verify Signature field, use the following:

```text title="Public Key"
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjquFIw98K+NToLJym3tmnljoEYZVt6zgWsNsc5u8+1lz+P/iuKpWtUvjSghkJh9lvqXU7DZI/iyzb9Ebc0obJHoWxJxr2T2xeiwrd9GO6+GEYHsOuD6r1ZxOonFpJ/zWZWNUUh0NSLexRjpQIKzUb2LhB1T3wukyCq/zuiSSMNI6Cd4wk20EMzorzq1XWb32FdkRN+11JZY9aNqlpVK1Miq7YnH2pshhWBhs4+pkOte2XOG28Z39yIC4M/3t/8tjBKyCo6PEs0vsPkfSTjYxjtuBeD9jJaOjWdMIX5UUHdlAUn7fYL4ONmiJkfIwVEZjyeiqZzTm1XVFqaj9jDr6PwIDAQAB
```

```text title="Private Key"
-----BEGIN RSA PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCOq4UjD3wr41OgsnKbe2aeWOgR
hlW3rOBaw2xzm7z7WXP4/+K4qla1S+NKCGQmH2W+pdTsNkj+LLNv0RtzShskehbEnGvZPbF6LCt3
0Y7r4YRgew64PqvVnE6icWkn/NZlY1RSHQ1It7FGOlAgrNRvYuEHVPfC6TIKr/O6JJIw0joJ3jCT
bQQzOivOrVdZvfYV2RE37XUllj1o2qWlUrUyKrticfamyGFYGGzj6mQ617Zc4bbxnf3IgLgz/e3/
y2MErIKjo8SzS+w+R9JONjGO24F4P2Mlo6NZ0whflRQd2UBSft9gvg42aImR8jBURmPJ6KpnNObV
dUWpqP2MOvo/AgMBAAECggEABuqHrLhuc440mqCr75+ezORQc7EIbLwDsEKy+jO9iI3AknyNGBih
1W4VWZxohnSVMRXG6aCED1ZJaI1BgGhCQpVsjyFqFQDpnpuPi+JrxEGNckPk5ceb+uH16egHifm2
xvl2t/hSkYjeHiJrifn23mNztzBGRnuZgm0fKpHlSFqGEEJjXUpubVlJ/zKJxiQz+TjdizDTy6gk
LNCwncloKCImaFijyelZ4iVWBVPv36dsSm9S4vNnC8yW7WO2z4GAfpE1Y9VImhS3jwK54/Ia5oTB
29f377MwmL0sY9bob5HPbyeqdfcmsOWEcC46IPwrogTnaNg+LkbeQrjIWUlMCQKBgQC/7MiTcPmP
kKbUPY9/Kqla8JPps0Iz1StrQpBehx4PsIp+boGCdyjemiJhT048wpRHfqEILtdmJnRE0GZqY7Mv
rWmjwm/BQZA3TCWXAXGLTAw1wmdS2CP+4KsEguyFP9mUjGuXLoPAbXiSxITLSlhgwwZIC7iT6WJ9
24LFmVCthQKBgQC+TRK+R0rJLilaRHFTqDFdELxE7NPy3yDIPeklJ9+PORR4YVypKaYifY+I/R/i
hueoacQpdfXkfUDZZ2hwk0lF8vbOrg/MYRu0pTz97Mx6YCsLhVlpNVCPcqXejYF0erSSJwEFgaEm
ifz9rQ+8nHqnO2DwhO5sBV8Lr5s2vBHB8wKBgGhK5m/gm2ydYVrCHSEwcJkfVHFRXO9HrnF52XPU
nsxN1eSAblYUJJxaS8ZvTweLgQIc2KrWsWwsB1CBorW7edq1tEst1IbC9vhlo6OcQDQ+3f+0pWsK
Uv0k3ynzb021danYaHrd5vCBTF0M91B1FPN35wjtfZ662y+jQjvYZVP1AoGAbto2sOCWj9pz/EEi
QrkXCD9XbE8Ip9GSJxLpXNt9PtDhO757W48HV9AMbKAGks5C47e4rO4p7o+H1xyFmg4yAK0nV/3M
9iEbIn+ep8vo0OB0MqHbE44a/3SpaprDbjaMORa/YZXBadG3rY3CPPxp9kCAl5rXx9TZKNWCdL/Z
GEECgYBBIIXLiGXkhT8Ih9NipwdU9TWiMi4QdYIjBEveaUrmKomZV9vpOX2bO8QbG9cFaXZ7JrbM
yjgZ+9gkcESW2cGQkCDt0NB4R37w1v1SzHJ3FP0TBl1Xyb4nUyaGYLqCRFcplECmDh1WT7D++ElH
gNhmwBM0tURs038rRvqbRTSqJQ==
-----END RSA PRIVATE KEY-----
```

### Auth Token

The token is a three-part dot-separated base64-encoded text on the right of the form (in the Encoded field).

```text
eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJYamFjZWtAamFwaWxhLnBsIiwiaXNzIjoiaW50ZXJuYWwifQ.grJ8Imy2HsSUJtvyYItkaksZMHTI-g03EwO_SXq1yuEHVMpJVPE6FOJIJM3RNrtu09brJ71t5riHpoQxgewZw5_yEkR0epDPv_ns8TrrKxvvzghY_p161nIkJqDMhI-puW6H_v4iuoQ9YazgC6zhRCPyK2Fv_mrHBA2SqJaYIvYzVevH4dYO-faOpuyd5cOfN41rni3kWNHgwynAfMZkq4Y6EBzcq3NWpcG9Z1q_RQ_Uc04ZdWAdZZ8qUmqsXPKXTiwcs-2nboMdEl_bobXIcHRIbV0Tx-5RU62NcSNYDi1oA_fNwyz8Dn3QdA5l3f3-ixiJWTYPLgPTXI6bYifvUQ
```

!!! tip
    "Save" the token in `demo_token` environment variable for faster access.

    ```bash
    demo_token=[copy_the_token_here]
    ```

Use the token as the value of `--auth_token` of the [Unity Catalog CLI](../cli/index.md).

```bash
./bin/uc user list --auth_token $demo_token
```

## Create Permission to Create Schema for Demo User

```console
./bin/uc permission create \
    --auth_token $(cat etc/conf/token.txt) \
    --securable_type catalog \
    --name unity \
    --principal demo@unitycatalog.io \
    --privilege "USE CATALOG"
┌────────────────────┬───────────────┐
│     PRINCIPAL      │  PRIVILEGES   │
├────────────────────┼───────────────┤
│demo@unitycatalog.io│["USE CATALOG"]│
└────────────────────┴───────────────┘
```

```console
./bin/uc permission create \
    --auth_token $(cat etc/conf/token.txt) \
    --securable_type catalog \
    --name unity \
    --principal demo@unitycatalog.io \
    --privilege "CREATE SCHEMA"
┌────────────────────┬───────────────────────────────┐
│     PRINCIPAL      │          PRIVILEGES           │
├────────────────────┼───────────────────────────────┤
│demo@unitycatalog.io│["USE CATALOG","CREATE SCHEMA"]│
└────────────────────┴───────────────────────────────┘
```

```console
./bin/uc permission get \
    --auth_token $(cat etc/conf/token.txt) \
    --securable_type catalog \
    --name unity
┌────────────────────┬───────────────────────────────┐
│     PRINCIPAL      │          PRIVILEGES           │
├────────────────────┼───────────────────────────────┤
│demo@unitycatalog.io│["USE CATALOG","CREATE SCHEMA"]│
└────────────────────┴───────────────────────────────┘
```

## Create Schema as Demo User

As `demo` user, create a new schema.

```console
$ ./bin/uc schema create \
    --auth_token $demo_token \
    --catalog unity \
    --name demo_schema
┌───────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────┐
│                    KEY                    │                                        VALUE                                         │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│NAME                                       │demo_schema                                                                           │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME                               │unity                                                                                 │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT                                    │null                                                                                  │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES                                 │{}                                                                                    │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│FULL_NAME                                  │unity.demo_schema                                                                     │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│OWNER                                      │demo@unitycatalog.io                                                                  │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT                                 │1731442653861                                                                         │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_BY                                 │demo@unitycatalog.io                                                                  │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT                                 │1731442653861                                                                         │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_BY                                 │demo@unitycatalog.io                                                                  │
├───────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_ID                                  │8fade42e-0913-4c5b-9de4-b99317e7bc14                                                  │
└───────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘
```

## Create Table as Demo User

```console
$ ./bin/uc table create \
    --auth_token $demo_token \
    --full_name unity.demo_schema.only_demo_can_access \
    --columns "id INT, name STRING" \
    --storage_location /tmp/only_demo_can_access
Table created successfully at: file:///tmp/only_demo_can_access
┌───────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    KEY                    │                                                                                              VALUE                                                                                              │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                                       │only_demo_can_access                                                                                                                                                                             │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME                               │unity                                                                                                                                                                                            │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME                                │demo_schema                                                                                                                                                                                      │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_TYPE                                 │EXTERNAL                                                                                                                                                                                         │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_SOURCE_FORMAT                         │DELTA                                                                                                                                                                                            │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COLUMNS                                    │{"name":"id","type_text":"int","type_json":"{\"name\":\"id\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}}","type_name":"INT","type_precision":0,"type_scale":0,"type_interval_type":nu│
│                                           │ll,"position":0,"comment":null,"nullable":true,"partition_index":null}                                                                                                                           │
│                                           │{"name":"name","type_text":"string","type_json":"{\"name\":\"name\",\"type\":\"string\",\"nullable\":true,\"metadata\":{}}","type_name":"STRING","type_precision":0,"type_scale":0,"type_interval│
│                                           │_type":null,"position":1,"comment":null,"nullable":true,"partition_index":null}                                                                                                                  │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│STORAGE_LOCATION                           │file:///tmp/only_demo_can_access/                                                                                                                                                                │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT                                    │null                                                                                                                                                                                             │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES                                 │{}                                                                                                                                                                                               │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│OWNER                                      │demo@unitycatalog.io                                                                                                                                                                             │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT                                 │1731442741539                                                                                                                                                                                    │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_BY                                 │demo@unitycatalog.io                                                                                                                                                                             │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT                                 │1731442741539                                                                                                                                                                                    │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_BY                                 │demo@unitycatalog.io                                                                                                                                                                             │
├───────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID                                   │ca25299a-a588-47af-b8a2-8660f3c89d34                                                                                                                                                             │
└───────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## List Tables

Only `demo` (the owner) and `admin` users can list the tables under `unity.demo_schema` schema.

```console
$ ./bin/uc table list --catalog unity --schema demo_schema --auth_token $demo_token
┌────────────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬────────────────────────────────────┐
│        NAME        │ CATALOG_NAME │ SCHEMA_NAME  │  TABLE_TYPE  │DATA_SOURCE_FO│   COLUMNS    │STORAGE_LOCATI│   COMMENT    │  PROPERTIES  │    OWNER     │  CREATED_AT  │  CREATED_BY  │  UPDATED_AT  │  UPDATED_BY  │              TABLE_ID              │
│                    │              │              │              │     RMAT     │              │      ON      │              │              │              │              │              │              │              │                                    │
├────────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼────────────────────────────────────┤
│only_demo_can_access│unity         │demo_schema   │EXTERNAL      │DELTA         │[{"name":"i...│file:///tmp...│null          │{}            │demo@unityc...│1731442741539 │demo@unityc...│1731442741539 │demo@unityc...│ca25299a-a588-47af-b8a2-8660f3c89d34│
└────────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴────────────────────────────────────┘
```

Others are not allowed.

```console
$ ./bin/uc table list --catalog unity --schema demo_schema --auth_token $token
[]
```

## Review Me

!!! note "FIXME: Likely to be removed"

!!! tip "subject_token"
    Use `subject_token` as specified in `etc/conf/token.txt`.

```bash
http --form http://localhost:8080/api/1.0/unity-control/auth/tokens \
    grant_type=urn:ietf:params:oauth:grant-type:token-exchange \
    requested_token_type=urn:ietf:params:oauth:token-type:access_token \
    subject_token_type=urn:ietf:params:oauth:token-type:id_token \
    subject_token=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJpbnRlcm5hbCIsInN1YiI6ImphY2VrQGphcGlsYS5wbCIsIm5hbWUiOiJKYWNlayBMYXNrb3dza2kifQ.im21f6LtBy
```

```text
$ echo $token
eyJraWQiOiJiOTk1YmMwYTUyN2ZmYmJmOWI0M2YxMDhhMWEwZDgyNWEwNWViNDA3MGIyODMxYTg4ZGZhZjM0ZDJlODc5NzMzIiwiYWxnIjoiUlM1MTIiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJqYWNla0BqYXBpbGEucGwiLCJpc3MiOiJpbnRlcm5hbCIsImlhdCI6MTczMTI2Nzk5NywianRpIjoiNzQ1ODI5OTgtMzNlOC00NzQ5LTk4NWQtOTJlMDhiMWMzMjYwIiwidHlwZSI6IkFDQ0VTUyJ9.M_5a8QmdnirdcJiOwJwZtqpJMv14mZyKfbOcF3i8B7X8Q3HNd8oqgSlieHuOfpBjXbHbQjYA-VefMc59rQVaAOc9LUMW0DpCDAF5hERjmMXKdBH9zgSGxGidOcm-NJLR-ZIh1hssGmQYZEk8YiJyitjrjwr_le3gp7VKEHgibd31RxkK-wumhCFLHoMWvcxjCh5D89p91J5T5wx2PSjtrShQ9vVns0bZ8uq2PQMNOpvGnFZk0OESuvVtAL92WVODYkeeMT2r8ieoTh9KqieQ_Vty1AddzrKU7_KWPiLsYfPgTrGrgGrGsmlmR8KHMBZBe90kMlEFkhJaNAEITfT6aQ
```

```bash
http --form http://localhost:8080/api/1.0/unity-control/auth/tokens \
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
