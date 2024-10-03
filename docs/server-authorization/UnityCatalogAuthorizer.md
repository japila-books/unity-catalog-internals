# UnityCatalogAuthorizer

`UnityCatalogAuthorizer` is an [abstraction](#contract) of [authorizers](#implementations).

## Contract (Subset)

### grantAuthorization { #grantAuthorization }

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
