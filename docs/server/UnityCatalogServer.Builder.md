# UnityCatalogServer.Builder

## ServerProperties { #serverProperties }

```java
ServerProperties serverProperties
```

`UnityCatalogServer.Builder` is given a [ServerProperties](ServerProperties.md) using [serverProperties](#serverProperties) accessor method.

`serverProperties` is used when:

* [UnityCatalogServer](UnityCatalogServer.md) is created and is requested to [setDefaults](UnityCatalogServer.md#setDefaults) and [initializeServer](UnityCatalogServer.md#initializeServer)

!!! danger "Open Question"
    Why does `UnityCatalogServer` require `serverProperties` to be created since all the methods that could use it accept a `UnityCatalogServer.Builder`?

### serverProperties

```java
UnityCatalogServer.Builder serverProperties(
  ServerProperties serverProperties)
```

`serverProperties` sets this [ServerProperties](#serverProperties).

---

`serverProperties` is used when:

* `UnityCatalogServer` is requested to [setDefaults](UnityCatalogServer.md#setDefaults)

## Build UnityCatalogServer { #build }

```java
UnityCatalogServer build()
```

`build` creates a [UnityCatalogServer](UnityCatalogServer.md).

---

`build` is used when:

* `UnityCatalogServer` is [launched as a command-line application](UnityCatalogServer.md#main)
