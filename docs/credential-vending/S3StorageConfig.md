# S3StorageConfig

`S3StorageConfig` represents a configuration of a bucket (_a container for objects_) in [Amazon S3](https://aws.amazon.com/s3/).

`S3StorageConfig` is a collection of the following properties:

* <span id="bucketPath"> Bucket Path
* <span id="region"> S3 Region
* <span id="awsRoleArn"> Role ARN
* <span id="accessKey"> Access Key
* <span id="secretKey"> Secret Key
* <span id="sessionToken"> Session Token

`S3StorageConfig` is created only when `ServerProperties` is requested for the [S3 configurations](../server/ServerPropertiesUtils.md#getS3Configurations).

`S3StorageConfig` is used by the following services:

* [AwsCredentialVendor](AwsCredentialVendor.md#s3Configurations) to [vendAwsCredentials](AwsCredentialVendor.md#vendAwsCredentials) and [getStsClientForStorageConfig](AwsCredentialVendor.md#getStsClientForStorageConfig)
* [FileIOFactory](../iceberg/FileIOFactory.md) to [getS3FileIO](../iceberg/FileIOFactory.md#getS3FileIO)
* [TableConfigService](../iceberg/TableConfigService.md#s3Configurations) to [getS3Config](../iceberg/TableConfigService.md#getS3Config)
