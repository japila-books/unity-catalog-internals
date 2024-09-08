# ModelService

`ModelService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/models` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | `/` | [listRegisteredModels](#listRegisteredModels) | <ul><li>catalog_name<li>schema_name<li>max_results<li>page_token</ul>
 POST | `/` | [createRegisteredModel](#createRegisteredModel) | `CreateRegisteredModel`
 DELETE | `/{full_name}` | [deleteRegisteredModel](#deleteRegisteredModel) | <ul><li>fullName<li>force</ul>
 GET | `/{full_name}` | [getRegisteredModel](#getRegisteredModel) | <ul><li>fullName</ul>
 PATCH | `/{full_name}` | [updateRegisteredModel](#updateRegisteredModel) | `UpdateRegisteredModel`
 GET | `/{full_name}/versions` | [listModelVersions](#listModelVersions) | <ul><li>full_name<li>max_results<li>page_token</ul>
 DELETE | `/{full_name}/versions/{version}` | [deleteModelVersion](#deleteModelVersion) | <ul><li>fullName<li>version</ul>
 GET | `/{full_name}/versions/{version}` | [getModelVersion](#getModelVersion) | <ul><li>full_name<li>version</ul>
 PATCH | `/{full_name}/versions/{version}` | [updateModelVersion](#updateModelVersion) | `UpdateModelVersion`
 PATCH | `/{full_name}/versions/{version}/finalize` | [finalizeModelVersion](#finalizeModelVersion) | `FinalizeModelVersion`
 POST | `/versions` | [createModelVersion](#createModelVersion) | `CreateModelVersion`

## ModelRepository { #MODEL_REPOSITORY }

`ModelService` gets the system-wide [ModelRepository](../persistent-storage/ModelRepository.md) when created.

## Register Model { #createRegisteredModel }

```java
HttpResponse createRegisteredModel(
  CreateRegisteredModel createRegisteredModel)
```

`createRegisteredModel` requests the [ModelRepository](#MODEL_REPOSITORY) instance to [register a model](../persistent-storage/ModelRepository.md#createRegisteredModel).

!!! note "Example"

    ```console
    $ http http://localhost:8081/api/2.1/unity-catalog/models | jq '.registered_models'
    []
    ```
