# TemporaryModelVersionCredentialsService

`TemporaryModelVersionCredentialsService` is an API service of [UnityCatalogServer](UnityCatalogServer.md) to handle HTTP requests at `/api/2.1/unity-catalog/temporary-model-version-credentials` URL.

Method | URL | Handler | Params
-|-|-|-
 POST | `/` | [generateTemporaryModelVersionCredentials](#generateTemporaryModelVersionCredentials) | JSON-ified `GenerateTemporaryModelVersionCredential`

`TemporaryModelVersionCredentialsService` supports [credential vending](#generateTemporaryModelVersionCredentials) for model versions in non-file-based storage locations.

## Creating Instance

`TemporaryModelVersionCredentialsService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)
* <span id="credentialOps"> [CredentialOperations](../credential-vending/CredentialOperations.md)

While being created, `TemporaryModelVersionCredentialsService` creates an [UnityAccessEvaluator](#evaluator).

`TemporaryModelVersionCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## UnityAccessEvaluator { #evaluator }

`TemporaryModelVersionCredentialsService` creates an [UnityAccessEvaluator](../server-authorization/UnityAccessEvaluator.md) (with the given [UnityCatalogAuthorizer](#authorizer)) when [created](#creating-instance).

## ModelRepository { #MODEL_REPOSITORY }

`TemporaryModelVersionCredentialsService` gets the system-wide [ModelRepository](../persistent-storage/ModelRepository.md#getInstance) instance when [created](#creating-instance).

`TemporaryModelVersionCredentialsService` uses the `ModelRepository` to [look up the model version](../persistent-storage/ModelRepository.md#getModelVersion) while [generating temporary model version credentials](#generateTemporaryModelVersionCredentials).

## Generate Temporary Model Version Credentials { #generateTemporaryModelVersionCredentials }

``` java
HttpResponse generateTemporaryModelVersionCredentials(
  GenerateTemporaryModelVersionCredential generateTemporaryModelVersionCredentials)
```

`generateTemporaryModelVersionCredentials`...FIXME

### Privileges by Model Version Operation { #modelVersionOperationToPrivileges }

```java
Set<CredentialContext.Privilege> modelVersionOperationToPrivileges(
  ModelVersionOperation modelVersionOperation)
```

`modelVersionOperationToPrivileges` converts the given [ModelVersionOperation](../credential-vending/index.md#model-version-operations) to [Privileges](../basic-server-access-control/index.md#privileges):

ModelVersionOperation | Privileges
-|-
 `READ_MODEL_VERSION` | `SELECT`
 `READ_WRITE_MODEL_VERSION` | `SELECT`, `UPDATE`
 `UNKNOWN_MODEL_VERSION_OPERATION` | A `BaseException` is thrown
