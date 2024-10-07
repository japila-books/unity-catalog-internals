# TemporaryModelVersionCredentialsService

## Creating Instance

`TemporaryModelVersionCredentialsService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)
* <span id="credentialOps"> [CredentialOperations](../credential-vending/CredentialOperations.md)

While being created, `TemporaryModelVersionCredentialsService` creates an [UnityAccessEvaluator](#evaluator).

`TemporaryModelVersionCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## UnityAccessEvaluator { #evaluator }

`TemporaryModelVersionCredentialsService` creates an [UnityAccessEvaluator](../server-authorization/UnityAccessEvaluator.md) (with the given [UnityCatalogAuthorizer](#authorizer)) when [created](#creating-instance).

## generateTemporaryModelVersionCredentials { #generateTemporaryModelVersionCredentials }

``` java
HttpResponse generateTemporaryModelVersionCredentials(
  GenerateTemporaryModelVersionCredential generateTemporaryModelVersionCredentials)
```

`generateTemporaryModelVersionCredentials`...FIXME
