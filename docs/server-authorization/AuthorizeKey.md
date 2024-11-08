# AuthorizeKey

`AuthorizeKey` defines authorization policies of the API services of [UnityCatalogServer](../server/UnityCatalogServer.md) for [Server Authorization](index.md):

* [CatalogService](../server/CatalogService.md)
* [FunctionService](../server/FunctionService.md)
* [ModelService](../server/ModelService.md)
* [PermissionService](../server/PermissionService.md)
* [SchemaService](../server/SchemaService.md)
* [Scim2UserService](../server/Scim2UserService.md)
* [TableService](../server/TableService.md)
* [TemporaryPathCredentialsService](../server/TemporaryPathCredentialsService.md)
* [VolumeService](../server/VolumeService.md)

!!! note
    `AuthorizeKey` is a Java annotation (see [9.6. Annotation Interfaces]({{ java.spec }}/jls-9.html#jls-9.6)).

Every operation of an API service is decorated with `AuthorizeKey` annotation for server authorization.

`AuthorizeKey` consists of a [SecurableType](../basic-server-access-control/index.md#securables) and an optional name of the securable.

`AuthorizeKey` maps request parameters to [SecurableType](../basic-server-access-control/index.md#securables)s (default: (empty)).

The Unity Catalog server uses [UnityAccessDecorator](UnityAccessDecorator.md) to [findAuthorizeKeys](UnityAccessDecorator.md#findAuthorizeKeys).
