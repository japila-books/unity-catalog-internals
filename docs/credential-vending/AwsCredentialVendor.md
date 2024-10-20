# AwsCredentialVendor

`AwsCredentialVendor` is used to [vend S3 bucket credentials](#vendAwsCredentials) for [CredentialOperations](CredentialOperations.md#awsCredentialVendor) (to [vend credentials](CredentialOperations.md#vendCredential) for `s3://` storage scheme).

`AwsCredentialVendor` uses [server.properties](../server/ServerProperties.md#getS3Configurations) configuration file for S3 bucket security configurations.

!!! note "AWS Security Token Service (STS)"
    `AwsCredentialVendor` uses [AWS Security Token Service (STS)](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html) to request [temporary, limited-privilege security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html):

    * An access key ID
    * A secret access key
    * A security (or session) token

## S3 Configurations { #s3Configurations }

```java
Map<String, S3StorageConfig> s3Configurations
```

`AwsCredentialVendor` initializes `s3Configurations` based on [server.properties](../server/ServerProperties.md#getS3Configurations) configuration file.

This `s3Configurations` is used to look up [S3StorageConfig](S3StorageConfig.md)s to [vend S3 bucket credentials](#vendAwsCredentials).

## Vend Credentials { #vendAwsCredentials }

```java
Credentials vendAwsCredentials(
  CredentialContext context)
```

`vendAwsCredentials` looks up the [S3 bucket](CredentialContext.md#getStorageBase) (of the given [CredentialContext](CredentialContext.md)) in the [S3 Configurations](#s3Configurations).

??? note "BaseException"
    `vendAwsCredentials` reports a `BaseException` when the given storage base could not be found:

    ```text
    S3 bucket configuration not found.
    ```

If a [session token](S3StorageConfig.md#getSessionToken) is defined, `vendAwsCredentials` returns a "static session" `Credentials` with the following:

* [Access Key](S3StorageConfig.md#getAccessKey)
* [Secret Key](S3StorageConfig.md#getSecretKey)
* [Session Token](S3StorageConfig.md#getSessionToken)

Otherwise (with no [session token](S3StorageConfig.md#getSessionToken) defined), `vendAwsCredentials` [gets an AWS STS client](#getStsClientForStorageConfig) to assume a role with the following:

Property | Value
-|-
 **Amazon Resource Name (ARN)** of the role to assume | [Role ARN](S3StorageConfig.md#getAwsRoleArn)
 **IAM policy** | [IAM policy](AwsPolicyGenerator.md#generatePolicy) for the [privileges](CredentialContext.md#getPrivileges) and the [locations](CredentialContext.md#getLocations)
 **Assumed Role Session** | `uc-[randomUUID]`
 Duration | 1 hour

In the end, `vendAwsCredentials` requests the `StsClient` for the temporary security credentials (an access key ID, a secret access key, and a security (or session) token).

---

`vendAwsCredentials` is used when:

* `CredentialOperations` is requested to [vend AWS credentials](CredentialOperations.md#vendAwsCredential)
