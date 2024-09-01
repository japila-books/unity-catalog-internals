# AuthCli

`AuthCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `auth` sub-commands](#handle).

```console
$ ./bin/uc auth --help
Please provide a valid sub-command for auth.
Valid sub-commands for auth are: login
For detailed help on auth sub-commands, use bin/uc auth <sub-command> --help
```

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

## Login { #login }

```java
String login(
  ApiClient apiClient,
  JSONObject json)
```

??? note "Static Method"
    `login` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`login`...FIXME
