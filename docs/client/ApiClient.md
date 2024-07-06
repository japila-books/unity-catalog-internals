# ApiClient

`ApiClient` is an API client of [Unity Catalog Localhost Reference Server](../server/index.md).

??? note "OpenAPI Generator"
    `ApiClient` was auto-generated using [OpenAPI Generator]({{ openapi.home }}) based on Unity Catalog's [OpenAPI specification]({{ uc.github }}/api/all.yaml).

    [sbt-openapi-generator]({{ openapi.github }}/sbt-openapi-generator) 7.5.0 is used in the `client` sbt module of the `unitycatalog` project.

`ApiClient` uses `http://localhost:8080/api/2.1/unity-catalog` as the [default base URI](#getDefaultBaseUri) (unless [overriden](#updateBaseUri)).

`ApiClient` is used by [UnityCatalogCli](../cli/UnityCatalogCli.md#getApiClient).

## updateBaseUri { #updateBaseUri }

```java
void updateBaseUri(
  String baseUri)
```

`updateBaseUri`...FIXME
