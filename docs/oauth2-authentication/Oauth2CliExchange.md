# Oauth2CliExchange

`Oauth2CliExchange` is a simple [OAuth2](https://oauth.net/2/) authentication flow for the [CLI](../cli/index.md) (to [login](../cli/AuthCli.md)).

## etc/conf/server.properties { #serverProperties }

`Oauth2CliExchange` loads `etc/conf/server.properties` into the [serverProperties](#serverProperties) when [created](#creating-instance).

!!! note
    The path `etc/conf/server.properties` is fixed and cannot be changed.

## Creating Instance

`Oauth2CliExchange` takes no arguments to be created.

While being created, `Oauth2CliExchange` loads `etc/conf/server.properties` into the [serverProperties](#serverProperties).

`Oauth2CliExchange` is created when:

* `AuthCli` is requested to [login](../cli/AuthCli.md#login)

## Authenticate { #authenticate }

```java
String authenticate()
```

`authenticate` returns an identity token.

---

`authenticate` reads the following server properties (from [etc/conf/server.properties](#serverProperties)):

* `server.authorization-url`
* `server.token-url`
* `server.client-id`
* `server.client-secret`
* [server.redirect-port](#findAvailablePort)

`authenticate` starts an `HttpServer` to listen on the port (based on [server.redirect-port](#findAvailablePort)) and an [AuthCallbackHandler](AuthCallbackHandler.md) to handle the root path `/`.

`authenticate` prints out the following message to the console:

```text
Listening on port: [port]
```

`authenticate` builds an auth URL as follows:

URL Part | Value
-|-
 `redirectUrl` | `server.authorization-url` configuration property
 `client_id` | `server.client-id` configuration property
 `redirect_uri` | `http://localhost:[port]`
 `response_type` | `code`
 `scope` | `openid profile email`
 `state` | Some random 16 bytes

`authenticate` prints out the following message to the console:

```text
Attempting to open the authorization page in your default browser.
If the browser does not open, you can manually open the following URL:
[authURL]
```

`authenticate` uses `/usr/bin/open` to open the auth URL (in the default browser).

!!! note
    Any exceptions while trying to open the browser with the auth URL are simply ignored.

`authenticate` requests the `AuthCallbackHandler` for the auth code.

`authenticate` prints out the following message to the console:

```text
Received authentication response.
```

`authenticate` stops the `HttpServer`.

`authenticate`...FIXME

---

`authenticate` is used when:

* `AuthCli` is requested to [login](../cli/AuthCli.md#login)
