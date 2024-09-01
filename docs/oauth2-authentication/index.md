# OAuth2 Authentication

Unity Catalog supports **OAuth2 Authentication**.

## Unity Catalog CLI

[Unity Catalog CLI](../cli/index.md) comes with [auth](../cli/AuthCli.md) sub-commands for OAuth2 authentication.

```console
❯ ./bin/uc auth --help
Please provide a valid sub-command for auth.
Valid sub-commands for auth are: login
For detailed help on auth sub-commands, use bin/uc auth <sub-command> --help
```

There is just a single [login](../cli/AuthCli.md#handle) sub-command supported.

```console
❯ ./bin/uc auth login --help
Usage: bin/uc auth login [options]
Required Params:
Optional Params:
  --server UC Server to connect to. Default is reference server.
  --auth_token PAT token to authorize uc requests.
  --output To indicate CLI output format preference. Supported values are json and jsonPretty.
  --identity_token Identity token to authorize
```

[login](../cli/AuthCli.md#handle) sub-command works differently based on `identity_token` optional param.
Unless specified on command line, [login](../cli/AuthCli.md#handle) uses [Oauth2CliExchange](Oauth2CliExchange.md) to [authenticate](Oauth2CliExchange.md#authenticate) and generate an identity token.

The identity token is used as `subject_token` query parameter for a POST request to `/auth/tokens` API endpoint with the other query parameters:

Query Parameter | Value
-|-
 `grant_type` | `urn:ietf:params:oauth:grant-type:token-exchange`
 `requested_token_type` | `urn:ietf:params:oauth:token-type:access_token`
 `subject_token_type` | `urn:ietf:params:oauth:token-type:id_token`
 `subject_token` | Identity token

That gives an `access_token` back.
