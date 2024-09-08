# ModelCli

`ModelCli` is used by [UnityCatalogCli](UnityCatalogCli.md) to [handle `registered_model` sub-commands](#handle).

```console
❯ ./bin/uc registered_model --help
Please provide a valid sub-command for registered_model.
Valid sub-commands for registered_model are: get, create, update, list, delete
For detailed help on registered_model sub-commands, use bin/uc registered_model <sub-command> --help
```

## Handle Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

`handle` creates a `RegisteredModelsApi` (with the given [ApiClient](../client/ApiClient.md)).

Subcommand | Handler | API Handlers
-|-|-
 `create` | [createRegisteredModel](#createRegisteredModel) | `RegisteredModelsApi`
 `list` | [listRegisteredModels](#listRegisteredModels) | `RegisteredModelsApi`
 `get` | [getRegisteredModel](#getRegisteredModel) | `RegisteredModelsApi`
 `update` | [updateRegisteredModel](#updateRegisteredModel) | `RegisteredModelsApi`
 `delete` | [deleteRegisteredModel](#deleteRegisteredModel) | `RegisteredModelsApi`

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `registered_model` command

## Create Registered Model { #createRegisteredModel }

```java
String createRegisteredModel(
  RegisteredModelsApi registeredModelsApi,
  JSONObject json)
```

`createRegisteredModel` deserializes (_converts_) the given `JSONObject` into `CreateRegisteredModel`.

`createRegisteredModel` requests the given `RegisteredModelsApi` to create a model (based on the `CreateRegisteredModel`).

!!! note "Example"

    ```bash
    ./bin/uc registered_model create \
        --catalog unity \
        --schema default \
        --name ccc \
        --comment 'This is a demo'
    ```

    ```text
    ┌───────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │              KEY              │                                                                VALUE                                                                 │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │NAME                           │ccc                                                                                                                                   │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │CATALOG_NAME                   │unity                                                                                                                                 │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │SCHEMA_NAME                    │default                                                                                                                               │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │STORAGE_LOCATION               │file:/tmp/ucroot/f029b870-9468-4f10-badc-630b41e5690d/b08dfd57-a939-46cf-b102-9b906b884fae/models/2e852506-4c70-4364-9c5e-d4a7ad9863ac│
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │FULL_NAME                      │unity.default.ccc                                                                                                                     │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │COMMENT                        │This is a demo                                                                                                                        │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │CREATED_AT                     │1725821472898                                                                                                                         │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │CREATED_BY                     │null                                                                                                                                  │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │UPDATED_AT                     │1725821472898                                                                                                                         │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │UPDATED_BY                     │null                                                                                                                                  │
    ├───────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │MODEL_ID                       │2e852506-4c70-4364-9c5e-d4a7ad9863ac                                                                                                  │
    └───────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    ```

!!! note
    `RegisteredModelsApi` sents `POST` HTTP requests to [/api/2.1/unity-catalog/models](../server/ModelService.md) endpoint.
