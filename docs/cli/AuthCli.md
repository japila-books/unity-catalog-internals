# AuthCli

`AuthCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `auth` sub-commands](#handle).

```console
$ ./bin/uc auth --help
Please provide a valid sub-command for auth.
Valid sub-commands for auth are: login
For detailed help on auth sub-commands, use bin/uc auth <sub-command> --help
```

## Exchange and Login

[login](#login) and [exchange](#exchange) use [doExchange](#doExchange) for authentication with the following difference:

* [login](#login) uses [Oauth2CliExchange](../oauth2-authentication/Oauth2CliExchange.md) to [authenticate](../oauth2-authentication/Oauth2CliExchange.md#authenticate) and generate an identity token.
* [exchange](#exchange) expects an identity token to be given (using `identity_token` parameter on command line).

## Handle Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

Subcommand | Handler
-|-
 `login` | One of the following based on `identity_token` param:<ul><li>[exchange](#exchange) for `identity_token` param</li><li>[login](#login)</li></ul>

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `auth` command

## Exchange

```java
String exchange(
  ApiClient apiClient,
  JSONObject json)
```

`exchange` de-serializes the given `json` object into a collection (that is supposed to include `identityToken` key based on `identity_token` CLI parameter).

`exchange` [doExchange](#doExchange) with the `identityToken` identity token.

## Login

```java
String login(
  ApiClient apiClient,
  JSONObject json)
```

`login`...FIXME

## doExchange { #doExchange }

```java
String doExchange(
  ApiClient apiClient,
  Map<String, String> login)
```

`doExchange` requests the given [ApiClient](../client/ApiClient.md) for the [base URI](../client/ApiClient.md#getBaseUri) to access `/auth/tokens` API endpoint with the following query parameters:

Query Parameter | Value
-|-
 `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange`
 `requested_token_type` | `urn:ietf:params:oauth:token-type:access_token`
 `subject_token_type` | `urn:ietf:params:oauth:token-type:id_token`
 `subject_token` | The value of `identityToken` in the given `login` collection

`doExchange` sends a POST request to `/auth/tokens` API endpoint with `application/x-www-form-urlencoded` content type.

In the end, `doExchange` creates a `LoginInfo` with `access_token` (from the response).
