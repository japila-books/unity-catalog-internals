# ServerProperties

## Creating Instance

`ServerProperties` takes no arguments to be created.

While being created, `ServerProperties` [loads the default server configuration](#generateDefaults).

`ServerProperties` is created once to be available [system-wide](#instance).

## ServerProperties Instance { #instance }

```java
ServerProperties instance
```

`ServerProperties` is available system-wide as one single instance.

```scala
import io.unitycatalog.server.utils.ServerProperties
val s3conf = ServerProperties.getInstance.getS3Configurations
```

This `ServerProperties` instance is used when:

* `UnityCatalogServer` is requested to [addApiServices](UnityCatalogServer.md#addApiServices)
* [FileUtils](../persistent-storage/FileUtils.md#properties) is created (and requested to [modifyS3Directory](../persistent-storage/FileUtils.md#modifyS3Directory))
* [HibernateUtils](../persistent-storage/HibernateUtils.md#properties) is created
* [UriUtils](../persistent-storage/UriUtils.md#properties) is created
* `AuthService` is requested to [grantToken](AuthService.md#grantToken)
* `IcebergRestCatalogService` is requested to handle [config](../iceberg/IcebergRestCatalogService.md#config) and write requests (see [server.iceberg-table.enabled](../iceberg/index.md#server.iceberg-table.enabled))
* `AwsCredentialVendor` is [created](../credential-vending/AwsCredentialVendor.md#s3Configurations)
* `AzureCredentialVendor` is [created](../credential-vending/AzureCredentialVendor.md#adlsConfigurations)
* `GcpCredentialVendor` is [created](../credential-vending/GcpCredentialVendor.md#gcsConfigurations)
* `FileIOFactory` is requested to [getS3FileIO](../iceberg/FileIOFactory.md#getS3FileIO)
* `TableConfigService` is [created](../iceberg/TableConfigService.md#s3Configurations)

## Server Properties { #properties }

`ServerProperties` [loads server configuration](#generateDefaults) from `etc/conf/server.properties` when [created](#creating-instance).

When there is no `etc/conf/server.properties`, the server properties are empty.

`ServerProperties` uses the properties for the following:

* [getProperty](#getProperty)
* [getS3Configurations](#getS3Configurations)
* [getGcsConfigurations](#getGcsConfigurations)
* [getAdlsConfigurations](#getAdlsConfigurations)

## Get Storage Configurations

### GCS { #getGcsConfigurations }

```java
Map<String, String> getGcsConfigurations()
```

`getGcsConfigurations` collects all non-empty `gcs.bucketPath.`- and `gcs.jsonKeyFilePath.`-prefixed configuration properties (from the [properties](#properties)).

`getGcsConfigurations` does so until there are no more pairs starting from `0`.

`getGcsConfigurations` returns a collection of pairs of `gcs.bucketPath.[n]` keys and `gcs.jsonKeyFilePath.[n]` values.

---

`getGcsConfigurations` is used when:

* `GcpCredentialVendor` is [created](../credential-vending/GcpCredentialVendor.md#gcsConfigurations)

### S3 { #getS3Configurations }

```java
Map<String, S3StorageConfig> getS3Configurations()
```

`getS3Configurations` creates a [S3StorageConfig](../credential-vending/S3StorageConfig.md) for every collection of `n`-indexed properties from the [server.properties](#properties) file (with `n` starting from `0`):

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

## Load Default Server Configuration { #generateDefaults }

```java
Properties generateDefaults()
```

?? note "Static Method"
    `generateDefaults` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`generateDefaults` takes all the server properties that have the default value defined.

## isAuthorizationEnabled { #isAuthorizationEnabled }

```java
boolean isAuthorizationEnabled()
```

`isAuthorizationEnabled` is enabled (`true`) when [server.authorization](./server-properties.md#AUTHORIZATION_ENABLED) server property is enabled.

---

`isAuthorizationEnabled` is used when:

* `ArmeriaServerBuilder` is [created](ArmeriaServerBuilder.md#authorizationEnabled)
* `UnityCatalogServer` is requested to [initialize](UnityCatalogServer.md#initializeServer) (and [initializes the authorizer](UnityCatalogServer.md#initializeAuthorizer) and [registers the Unity Catalog API security decorators](UnityCatalogServer.md#addSecurityDecorators))
* `AuthorizedService` is requested to [applyResponseFilter](AuthorizedService.md#applyResponseFilter)
* `AuthService` is requested to [create access token](AuthService.md#grantToken)

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.utils.ServerProperties` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.ServerProperties.name = io.unitycatalog.server.utils.ServerProperties
logger.ServerProperties.level = all
```

Refer to [Logging](../logging.md).
