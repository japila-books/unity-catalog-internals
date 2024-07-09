# PropertiesUtil

`PropertiesUtil` is a system-wide [configuration of S3 buckets](#loadProperties)

## Loading S3 Bucket Configuration { #loadProperties }

```java
void loadProperties()
```

`loadProperties` loads the key-value pairs from `etc/conf/server.properties` file into the [Properties](#properties).

`loadProperties` prints out the following DEBUG message to the logs:

```text
Properties loaded successfully
```

`loadProperties` creates a [S3BucketConfig](S3BucketConfig.md) for every tuple of the following properties:

* `s3.bucketPath.[n]`
* `s3.accessKey.[n]`
* `s3.secretKey.[n]`
* `s3.sessionToken.[n]`

!!! note
    `loadProperties` silently skips processing a tuple if any of the properties is undefined (`null`).

In the end, `loadProperties` registers the `S3BucketConfig`s by `s3.bucketPath`.

---

`loadProperties` is used when:

* `PropertiesUtil` is created

## Looking Up S3BucketConfig by S3 Path { #getS3BucketConfig }

```java
S3BucketConfig getS3BucketConfig(
  String s3Path)
```

`getS3BucketConfig` creates a URI for the given `s3Path`.

`getS3BucketConfig` creates a bucket path for the following URI parts (separated using `://`):

* Scheme
* Host

`getS3BucketConfig` uses the bucket path (`scheme://host`) to look up the `S3BucketConfig` in the [Properties](#properties).

---

`getS3BucketConfig` is used when:

* `TemporaryCredentialUtils` is requested to [find a S3 bucket config](../server/TemporaryCredentialUtils.md#findS3BucketConfig)
