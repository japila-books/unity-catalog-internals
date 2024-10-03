# TemporaryVolumeCredentialsService

## Creating Instance

`TemporaryVolumeCredentialsService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)
* <span id="credentialOps"> [CredentialOperations](CredentialOperations.md)

While being created, `TemporaryVolumeCredentialsService` creates an [UnityAccessEvaluator](#evaluator).

`TemporaryVolumeCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## UnityAccessEvaluator { #evaluator }

`TemporaryVolumeCredentialsService` creates an [UnityAccessEvaluator](../server-authorization/UnityAccessEvaluator.md) (with the given [UnityCatalogAuthorizer](#authorizer)) when [created](#creating-instance).
