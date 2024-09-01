# Oauth2CliExchange

`Oauth2CliExchange` is a simple [OAuth2](https://oauth.net/2/) authentication flow for the [CLI](../cli/index.md) (to [login](../cli/AuthCli.md)).

## Creating Instance

`Oauth2CliExchange` takes no arguments to be created.

While being created, `Oauth2CliExchange` loads `etc/conf/server.properties` into the [serverProperties](#serverProperties).

`Oauth2CliExchange` is created when:

* `AuthCli` is requested to [login](../cli/AuthCli.md#login)

## Authenticate { #authenticate }

```java
String authenticate()
```

`authenticate`...FIXME

---

`authenticate` is used when:

* `AuthCli` is requested to [login](../cli/AuthCli.md#login)
