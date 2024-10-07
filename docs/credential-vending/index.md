# Credential Vending

**Credential Vending** provides temporary, scoped credentials for secure access to the following Unity Catalog securables:

* [Model Versions](../server/TemporaryModelVersionCredentialsService.md#generateTemporaryModelVersionCredentials)
* [Paths](../server/TemporaryPathCredentialsService.md#generateTemporaryPathCredential)
* [Tables](../server/TemporaryTableCredentialsService.md#generateTemporaryTableCredential)
* [Volumes](../server/TemporaryVolumeCredentialsService.md#generateTemporaryTableCredential)

Credential Vending uses [CredentialOperations](CredentialOperations.md) to [vend credentials](CredentialOperations.md#vendCredential) to get temporary access to assets (data) stored in the following cloud object storages:

* Amazon S3
* Microsoft Azure
* Google Cloud

## Privileges

Credential Vending supports the following privileges:

* `SELECT`
* `UPDATE`

??? note "Permissions"
    Privileges is a synonym of Permissions.

## Learning Resources

1. [AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/)
