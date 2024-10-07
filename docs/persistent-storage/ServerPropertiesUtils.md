# ServerPropertiesUtils

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
