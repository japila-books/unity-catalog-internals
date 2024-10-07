# TemporaryCredentialUtils

## Looking Up AwsCredentials for S3 Storage Location { #findS3BucketConfig }

```java
AwsCredentials findS3BucketConfig(
  String storageLocation)
```

`findS3BucketConfig` requests the system-wide [PropertiesUtil](../persistent-storage/PropertiesUtil.md#instance) instance for [getS3BucketConfig](../persistent-storage/PropertiesUtil.md#getS3BucketConfig).

`findS3BucketConfig` creates an `AwsCredentials`.

Property | Value
-|-
 `accessKeyId` | [accessKey](../persistent-storage/S3BucketConfig.md#accessKey)
 `secretAccessKey` | [secretKey](../persistent-storage/S3BucketConfig.md#secretKey)
 `sessionToken` | [sessionToken](../persistent-storage/S3BucketConfig.md#sessionToken)

---

`findS3BucketConfig` is used when:

* `TemporaryTableCredentialsService` is requested to [generateTemporaryTableCredential](TemporaryTableCredentialsService.md#generateTemporaryTableCredential)
* `TemporaryVolumeCredentialsService` is requested to [generateTemporaryTableCredential](TemporaryVolumeCredentialsService.md#generateTemporaryTableCredential)
