# UnityCatalogAuthorizer

`UnityCatalogAuthorizer` is an [abstraction](#contract) of [authorizers](#implementations).

## Contract (Subset)

### Authorize { #authorize }

``` java
boolean authorize(
  UUID principal,
  UUID resource,
  Privileges action)
```

See:

* [JCasbinAuthorizer](JCasbinAuthorizer.md#authorize)

Used when:

* `PermissionService` is requested for the [authorizations](../server/PermissionService.md#getAuthorization)
* `UnityAccessEvaluator` is [created](UnityAccessEvaluator.md#authorizeHandle)

### Authorize All Privileges { #authorizeAll }

``` java
boolean authorizeAll(
  UUID principal,
  UUID resource,
  Privileges... actions)
```

See:

* [JCasbinAuthorizer](JCasbinAuthorizer.md#authorizeAll)

Used when:

* `UnityAccessEvaluator` is [created](UnityAccessEvaluator.md#authorizeAllHandle)

### Authorize Any Privileges { #authorizeAny }

``` java
boolean authorizeAny(
  UUID principal,
  UUID resource,
  Privileges... actions)
```

See:

* [JCasbinAuthorizer](JCasbinAuthorizer.md#authorizeAny)

Used when:

* `UnityAccessEvaluator` is [created](UnityAccessEvaluator.md#authorizeAnyHandle)

### Grant Authorization { #grantAuthorization }

```java
boolean grantAuthorization(
  UUID principal,
  UUID resource,
  Privileges action)
```

See:

* [JCasbinAuthorizer](JCasbinAuthorizer.md#grantAuthorization)

Used when:

* `UnityAccessUtil` is requested to [initializeAdmin](UnityAccessUtil.md#initializeAdmin)
* `CatalogService` is requested to [initializeAuthorizations](../server/CatalogService.md#initializeAuthorizations)
* `FunctionService` is requested to [initializeAuthorizations](../server/FunctionService.md#initializeAuthorizations)
* `ModelService` is requested to [initializeAuthorizations](../server/ModelService.md#initializeAuthorizations)
* `PermissionService` is requested to [updateAuthorization](../server/PermissionService.md#updateAuthorization)
* `SchemaService` is requested to [createAuthorizations](../server/SchemaService.md#createAuthorizations)
* `TableService` is requested to [initializeAuthorizations](../server/TableService.md#initializeAuthorizations)
* `VolumeService` is requested to [initializeAuthorizations](../server/VolumeService.md#initializeAuthorizations)

## Implementations

* [JCasbinAuthorizer](JCasbinAuthorizer.md)
* [AllowingAuthorizer](AllowingAuthorizer.md)
