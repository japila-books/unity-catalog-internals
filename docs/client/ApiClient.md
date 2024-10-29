# ApiClient

`ApiClient` is an API client of the [Unity Catalog Server](../server/index.md).

`ApiClient` uses `http://localhost:8080/api/2.1/unity-catalog` as the [default base URI](#getDefaultBaseUri) (unless [overriden](#updateBaseUri)).

`ApiClient` is used by [UnityCatalogCli](../cli/UnityCatalogCli.md#getApiClient).

## updateBaseUri { #updateBaseUri }

```java
void updateBaseUri(
  String baseUri)
```

`updateBaseUri`...FIXME
