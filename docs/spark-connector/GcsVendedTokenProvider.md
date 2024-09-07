# GcsVendedTokenProvider

`GcsVendedTokenProvider` is an `AccessTokenProvider` to provide access tokens for [UCSingleCatalog](UCSingleCatalog.md) to [load tables](UCSingleCatalog.md#loadTable) from [Google Cloud Storage](https://cloud.google.com/storage).

`GcsVendedTokenProvider` can be configured in a Spark application using the following configuration:

```text
spark.hadoop.fs.AbstractFileSystem.gs.impl     com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS
spark.hadoop.fs.gs.auth.access.token.provider  io.unitycatalog.connectors.spark.GcsVendedTokenProvider
spark.hadoop.fs.gs.auth.type                   ACCESS_TOKEN_PROVIDER
```

## getAccessToken { #getAccessToken }

??? note "AccessTokenProvider"

    ```java
    AccessToken getAccessToken()
    ```

    `getAccessToken` is part of the `AccessTokenProvider` abstraction.

`getAccessToken` creates a new `AccessToken` based on the following Hadoop Configuration properties:

Property | Hadoop Property
-|-
 `token` | `fs.gs.auth.access.token.credential`
 `expirationTime` | `fs.gs.auth.access.token.expiration`
