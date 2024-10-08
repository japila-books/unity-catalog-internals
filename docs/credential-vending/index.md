# Credential Vending

**Credential Vending** provides temporary, down-scoped credentials for secure access to the following Unity Catalog securables:

* [Model Versions](../server/TemporaryModelVersionCredentialsService.md#generateTemporaryModelVersionCredentials)
* [Paths](../server/TemporaryPathCredentialsService.md#generateTemporaryPathCredential)
* [Tables](../server/TemporaryTableCredentialsService.md#generateTemporaryTableCredential)
* [Volumes](../server/TemporaryVolumeCredentialsService.md#generateTemporaryTableCredential)

Credential Vending uses [CredentialOperations](CredentialOperations.md) to [vend credentials](CredentialOperations.md#vendCredential) to get temporary access to assets (data) stored in the following cloud object storages:

* [Amazon S3](#amazon-s3)
* Microsoft Azure
* Google Cloud

## Privileges

Credential Vending supports the following privileges:

* `SELECT`
* `UPDATE`

??? note "Permissions"
    Privileges is a synonym of Permissions.

## Amazon S3

[Alex Reid once wrote]({{ uc.slack }}/C076YREKX8W/p1728333073156489?thread_ts=1728308961.254459&cid=C076YREKX8W):

> For UC OSS to work with S3, you need a role (you give the arn of that role in the properties) that has access to the bucket (also set in the properties) and you also need a user that can assume that role (and you provide the creds for that user in the properties)
>
> In order to properly downscope vended credentials (when asking for creds to a specific table, etc.), we need to be able to assume a role that has broader bucket access.
>
> UC OSS doesn't yet support more advanced AWS access-like identity federation, etc.

And [later Alex wrote]({{ uc.slack }}/C076YREKX8W/p1728405322352489?thread_ts=1728308961.254459&cid=C076YREKX8W):

> you need to set a `roleArn` in the `server.properties` that has access to the bucket AND which the instance profile attached to the server can assume.
>
> This is how scoped AWS credentials work (you need to assume a role that has access to the bucket in order to give scoped temporary credentials)

## Learning Resources

1. [AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/)
