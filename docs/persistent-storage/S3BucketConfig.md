# S3BucketConfig

`S3BucketConfig` is a S3 bucket configuration.

`S3BucketConfig` is used when:

* `TemporaryCredentialUtils` is requested to [findS3BucketConfig](../server/TemporaryCredentialUtils.md#findS3BucketConfig)
* `PropertiesUtil` is requested to [getS3BucketConfig](PropertiesUtil.md#getS3BucketConfig)

## Creating Instance

`S3BucketConfig` takes the following to be created:

* <span id="bucketPath"> `bucketPath`
* <span id="accessKey"> `accessKey`
* <span id="secretKey"> `secretKey`
* <span id="sessionToken"> `sessionToken`

`S3BucketConfig` is created when:

* `PropertiesUtil` is requested to [loadProperties](PropertiesUtil.md#loadProperties)
