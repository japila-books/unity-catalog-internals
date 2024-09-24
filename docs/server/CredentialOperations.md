# CredentialOperations

## AwsCredentialVendor { #awsCredentialVendor }

[AwsCredentialVendor](AwsCredentialVendor.md) is created alongside `CredentialOperations`.

## AzureCredentialVendor { #azureCredentialVendor }

## GcpCredentialVendor { #gcpCredentialVendor }

## vendCredential { #vendCredential }

```java
TemporaryCredentials vendCredential(
  String path,
  Set<CredentialContext.Privilege> privileges)
TemporaryCredentials vendCredential(
  CredentialContext context)
```

`vendCredential`...FIXME

---

`vendCredential` is used when:

* `TemporaryModelVersionCredentialsService` is requested to [generateTemporaryModelVersionCredentials](TemporaryModelVersionCredentialsService.md#generateTemporaryModelVersionCredentials)
* `TemporaryPathCredentialsService` is requested to [generateTemporaryPathCredential](TemporaryPathCredentialsService.md#generateTemporaryPathCredential)
* `TemporaryTableCredentialsService` is requested to [generateTemporaryTableCredential](TemporaryTableCredentialsService.md#generateTemporaryTableCredential)
* `TemporaryVolumeCredentialsService` is requested to [generateTemporaryTableCredential](TemporaryVolumeCredentialsService.md#generateTemporaryTableCredential)
