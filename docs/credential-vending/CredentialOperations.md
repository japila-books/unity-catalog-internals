# CredentialOperations

## AwsCredentialVendor { #awsCredentialVendor }

[AwsCredentialVendor](AwsCredentialVendor.md) is created alongside `CredentialOperations`.

## AzureCredentialVendor { #azureCredentialVendor }

## GcpCredentialVendor { #gcpCredentialVendor }

[GcpCredentialVendor](GcpCredentialVendor.md) is created alongside `CredentialOperations`.

## Vend Credentials { #vendCredential }

```java
TemporaryCredentials vendCredential(
  String path,
  Set<CredentialContext.Privilege> privileges) // (1)!
TemporaryCredentials vendCredential(
  CredentialContext context)
```

1. Uses a [new CredentialContext](CredentialContext.md#create) for the given storage location (`path`) and the `privileges`.

??? note "BaseException"
    `vendCredential` throws a `BaseException` when the `path` is undefined (`null` or empty).

!!! note "Storage Location"
    The input `path` is also known as a storage location.

`vendCredential` [creates a CredentialContext](CredentialContext.md#create) for the given storage location (`path`) and the `privileges`.

`vendCredential` creates a `TemporaryCredentials` model with Cloud Provider-specific settings (based on the storage scheme of the `CredentialContext`).

Storage Scheme | Credential Vending Mechanism | TemporaryCredentials
-|-|-
`abfs` or `abfss` | [AzureCredential](#vendAzureCredential) | `AzureUserDelegationSAS`<ul><li>`sasToken`<li>`expirationTime`</ul>
`gs` | [AccessToken](#vendGcpToken) | `GcpOauthToken`<ul><li>`oauthToken`<li>`expirationTime`</ul>
`s3` | [Credentials](#vendAwsCredential) | `AwsCredentials`<ul><li>`accessKeyId`<li>`secretAccessKey`<li>`sessionToken`</ul>

---

`vendCredential` is used when:

* `TemporaryModelVersionCredentialsService` is requested to [generateTemporaryModelVersionCredentials](../server/TemporaryModelVersionCredentialsService.md#generateTemporaryModelVersionCredentials)
* `TemporaryPathCredentialsService` is requested to [generateTemporaryPathCredential](../server/TemporaryPathCredentialsService.md#generateTemporaryPathCredential)
* `TemporaryTableCredentialsService` is requested to [generateTemporaryTableCredential](../server/TemporaryTableCredentialsService.md#generateTemporaryTableCredential)
* `TemporaryVolumeCredentialsService` is requested to [generateTemporaryTableCredential](../server/TemporaryVolumeCredentialsService.md#generateTemporaryTableCredential)
