# CredentialContext

## Create CredentialContext { #create }

``` java
CredentialContext create(
  URI locationURI,
  Set<Privilege> privileges)
```

`create` builds a `CredentialContext` for the given `privileges` and the storage `locationURI`.

`CredentialContext` holds the following extra information based on the storage `locationURI`:

URI Component | Value
-|-
**Storage Scheme** | The `[<scheme>:]<scheme-specific-part>[#<fragment>]` part
**Storage Base** | The `[<scheme>:]<scheme-specific-part>[#<fragment>]` part followed by `://` and `[//<authority>]<path>[?<query>]`
**Locations** | The storage `locationURI`

??? note "Static Method"

    `create` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

---

`create` is used when:

* `CredentialOperations` is requested to [vend credentials](CredentialOperations.md#vendCredential)
* `FileIOFactory` is requested to [getCredentialContextFromTableLocation](../iceberg/FileIOFactory.md#getCredentialContextFromTableLocation)
* `TableConfigService` is requested to [getTableConfig](../iceberg/TableConfigService.md#getTableConfig)
