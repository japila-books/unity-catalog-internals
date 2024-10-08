# ServerPropertiesUtils

## Creating Instance

`ServerPropertiesUtils` takes no arguments to be created.

While being created, `ServerPropertiesUtils` [loads server configuration](#loadProperties).

`ServerPropertiesUtils` is created once to be available [system-wide](#instance).

## ServerPropertiesUtils Instance { #instance }

``` java
ServerPropertiesUtils instance
```

`ServerPropertiesUtils` is available system-wide as one single instance.

``` scala
import io.unitycatalog.server.persist.utils.ServerPropertiesUtils
val s3conf = ServerPropertiesUtils.getInstance.getS3Configurations
```

This `ServerPropertiesUtils` instance is used when:

* `UnityCatalogServer` is requested to [addServices](UnityCatalogServer.md#addServices)
* [FileUtils](../persistent-storage/FileUtils.md#properties) is created (and requested to [modifyS3Directory](../persistent-storage/FileUtils.md#modifyS3Directory))
* [HibernateUtils](../persistent-storage/HibernateUtils.md#properties) is created
* [UriUtils](../persistent-storage/UriUtils.md#properties) is created
* `AuthService` is requested to [grantToken](AuthService.md#grantToken)
* `AwsCredentialVendor` is [created](../credential-vending/AwsCredentialVendor.md#s3Configurations)
* `AzureCredentialVendor` is [created](../credential-vending/AzureCredentialVendor.md#adlsConfigurations)
* `GcpCredentialVendor` is [created](../credential-vending/GcpCredentialVendor.md#gcsConfigurations)
* `FileIOFactory` is requested to [getS3FileIO](../iceberg/FileIOFactory.md#getS3FileIO)
* `TableConfigService` is [created](../iceberg/TableConfigService.md#s3Configurations)

## Server Properties { #properties }

`ServerPropertiesUtils` [loads server configuration](#loadProperties) from `etc/conf/server.properties` when [created](#creating-instance).

When there is no `etc/conf/server.properties`, the server properties are empty.

`ServerPropertiesUtils` uses the properties for the following:

* [getProperty](#getProperty)
* [getS3Configurations](#getS3Configurations)
* [getGcsConfigurations](#getGcsConfigurations)
* [getAdlsConfigurations](#getAdlsConfigurations)

## getGcsConfigurations { #getGcsConfigurations }

``` java
Map<String, String> getGcsConfigurations()
```

`getGcsConfigurations` collects all non-empty `gcs.bucketPath.`- and `gcs.jsonKeyFilePath.`-prefixed configuration properties (from the [properties](#properties)).

`getGcsConfigurations` does so until there are no more pairs starting from `0`.

`getGcsConfigurations` returns a collection of pairs of `gcs.bucketPath.[n]` keys and `gcs.jsonKeyFilePath.[n]` values.

---

`getGcsConfigurations` is used when:

* `GcpCredentialVendor` is [created](../credential-vending/GcpCredentialVendor.md#gcsConfigurations)

## getS3Configurations { #getS3Configurations }

``` java
Map<String, S3StorageConfig> getS3Configurations()
```

`getS3Configurations` creates a `S3StorageConfig` for every collection of `n`-indexed properties from the [server.properties](#properties) file (with `n` starting from `0`):

* `s3.bucketPath.[n]`
* `s3.region.[n]`
* `s3.awsRoleArn.[n]`
* `s3.accessKey.[n]`
* `s3.secretKey.[n]`
* `s3.sessionToken.[n]`

`getS3Configurations` returns `S3StorageConfig`s by their `bucketPath`s.

!!! note
    `getS3Configurations` disregards a `S3StorageConfig` when the following hold true:

    * Any of `bucketPath`, `region` and `awsRoleArn` is undefined
    * Any of `accessKey`, `secretKey`, `sessionToken` is undefined

---

`getS3Configurations` is used when:

* `AwsCredentialVendor` is [created](../credential-vending/AwsCredentialVendor.md#s3Configurations)
* `FileIOFactory` is requested to [getS3FileIO](../iceberg/FileIOFactory.md#getS3FileIO)
* `TableConfigService` is [created](../iceberg/TableConfigService.md#s3Configurations)

## Load Server Configuration { #loadProperties }

```java
void loadProperties()
```

`loadProperties` loads `etc/conf/server.properties` file into the [Properties](#properties).

!!! note
    `loadProperties` prints out the following ERROR message to the logs when `etc/conf/server.properties` file could not be found:

    ``` text
    Properties file not found: [path]
    ```

    It is not a fatal error when there is no server configuration file.
    The [server properties](#properties) are simply empty.

`loadProperties` prints out the following DEBUG message to the logs:

```text
Properties loaded successfully
```

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.persist.utils.ServerPropertiesUtils` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.ServerPropertiesUtils.name = io.unitycatalog.server.persist.utils.ServerPropertiesUtils
logger.ServerPropertiesUtils.level = all
```

Refer to [Logging](../logging.md).
