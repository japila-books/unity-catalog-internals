# Server Authorization

**Server Authorization** can be enabled in [Unity Catalog Server](../server/index.md) using [server.authorization](#server.authorization) property in `etc/conf/server.properties` configuration file.

With Server Authorization enabled, the UC server uses [AuthDecorator](AuthDecorator.md) to enforce permission to access the API services based on [Bearer Authentication](#bearer-authentication) or `UC_TOKEN` cookie.

## server.authorization { #server.authorization }

To enable the server authorization `server.authorization` property should be `enable` (case-insensitive).

With server authorization enabled, Unity Catalog Server registers [AuthDecorator](AuthDecorator.md) to intercept all requests to `/api/2.1/unity-catalog/`-prefixed URLs.

With server authorization enabled, Unity Catalog Server uses [JCasbinAuthorizer](JCasbinAuthorizer.md) for role-based access control (RBAC).

## UnityAccessDecorator

Unity Catalog Server uses [UnityAccessDecorator](UnityAccessDecorator.md) to enforce Role-Based Access Control (RBAC).

## Bearer Authentication

??? note "OpenAPI Guide"
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

[Unity Catalog CLI](../cli/index.md) uses [auth_token](../cli/UnityCatalogCli.md#auth_token) command-line option to assign a personal access token for authentication.

```text
./bin/uc --auth_token
```

!!! note "etc/conf/token.txt"
	A sample personal access token is available as `etc/conf/token.txt`.

	```text
	./bin/uc --auth_token $(cat etc/conf/token.txt)
	```

## Demo

[Demo: Unity Catalog Server Authorization](../demo/unity-catalog-server-authorization.md)
