# TemporaryPathCredentialsService

## Creating Instance

`TemporaryPathCredentialsService` takes the following to be created:

* <span id="credentialOps"> [CredentialOperations](../credential-vending/CredentialOperations.md)

`TemporaryPathCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## Generate Temporary Path Credentials { #generateTemporaryPathCredential }

``` java
HttpResponse generateTemporaryPathCredential(
  GenerateTemporaryPathCredential generateTemporaryPathCredential)
```

`generateTemporaryPathCredential`...FIXME
