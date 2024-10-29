# Client API

Client API uses Unity Catalog's [OpenAPI specification]({{ uc.github }}/api/all.yaml) to generate the required classes (using [OpenAPI Generator](#openapi-generator)) to communicate with [Unity Catalog Server](../server/index.md).

The main communication client is [ApiClient](ApiClient.md).

## OpenAPI Generator

All the classes in `io.unitycatalog.client.api` Java package (e.g., [ApiClient](ApiClient.md), [GrantsApi](GrantsApi.md)) are auto-generated using [OpenAPI Generator]({{ openapi.home }}) based on Unity Catalog's [OpenAPI specification]({{ uc.github }}/api/all.yaml).

[sbt-openapi-generator]({{ openapi.github }}/sbt-openapi-generator) 7.5.0 is used in the `client` sbt module of the `unitycatalog` project.
