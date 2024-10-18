# MetastoreRepository

## Init Metastore If Needed { #initMetastoreIfNeeded }

```java
MetastoreDAO initMetastoreIfNeeded()
```

`initMetastoreIfNeeded` starts a transaction (with a new `Session` (Hibernate) from the system-wide [SessionFactory](HibernateUtils.md#SESSION_FACTORY)).

`initMetastoreIfNeeded` [looks up the one and only metastore](#getMetastoreDAO).

Unless found, `initMetastoreIfNeeded` creates a new metastore.

`initMetastoreIfNeeded` prints out the following INFO message to the logs:

```text
No metastore found, initializing a metastore for the server...
```

`initMetastoreIfNeeded` creates a `MetastoreDAO` with a pseudo-randomly generated UUID and persists it.

`initMetastoreIfNeeded` prints out the following INFO message to the logs:

```text
Server initialized with metastore id: [id]
```

---

In case of any exception, `initMetastoreIfNeeded` prints out the following ERROR message to the logs:

```text
Failed to initialize metastore
```

---

`initMetastoreIfNeeded` is used when:

* `UnityCatalogServer` is requested to [start](../server/UnityCatalogServer.md#start)

## System-Wide MetastoreRepository Instance { #INSTANCE }

```java
MetastoreRepository INSTANCE
```

`MetastoreRepository` creates an instance of itself at the class load time.

??? note "Final Property"
    `INSTANCE` is a Java **final property** to prevent [subclasses](#implementations) from overriding or hiding it.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.3).

??? note "Static Property"
    `INSTANCE` is a Java **class property** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

This `MetastoreRepository` instance is available using [MetastoreRepository.getInstance](#getInstance).

### Get Instance { #getInstance }

```java
MetastoreRepository getInstance()
```

??? note "Static Method"
    `getInstance` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`getInstance` returns the [system-wide MetastoreRepository Instance](#INSTANCE).

---

`getInstance` is used when:

* `UnityCatalogServer` is requested to [start](../server/UnityCatalogServer.md#start)
* `KeyMapperUtil` is requested to [mapResourceKeys](../server-authorization/KeyMapperUtil.md#mapResourceKeys)
* `UnityAccessUtil` is requested for the [MetastoreRepository](../server-authorization/UnityAccessUtil.md#METASTORE_REPOSITORY)
* `CatalogService` is requested to [filterCatalogs](../server/CatalogService.md#filterCatalogs)
* `FunctionService` is requested to [filterFunctions](../server/FunctionService.md#filterFunctions)
* `MetastoreService` is requested for the [MetastoreRepository](../server/MetastoreService.md#METASTORE_REPOSITORY)
* `ModelService` is requested to [filterModels](../server/ModelService.md#filterModels)
* `PermissionService` is requested for the [MetastoreRepository](../server/PermissionService.md#METASTORE_REPOSITORY)
* `SchemaService` is requested to [filterSchemas](../server/SchemaService.md#filterSchemas)
* `TableService` is requested to [filterTables](../server/TableService.md#filterTables)
* `VolumeService` is requested to [filterVolumes](../server/VolumeService.md#filterVolumes)
