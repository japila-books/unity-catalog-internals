# AuthorizeExpression

`AuthorizeExpression` is a Java annotation for an authorization expression of the API services:

* [CatalogService](../server/CatalogService.md)
* [FunctionService](../server/FunctionService.md)
* [ModelService](../server/ModelService.md)
* [PermissionService](../server/PermissionService.md)
* [SchemaService](../server/SchemaService.md)
* [Scim2UserService](../server/Scim2UserService.md)
* [TableService](../server/TableService.md)
* [TemporaryPathCredentialsService](../server/TemporaryPathCredentialsService.md)
* [VolumeService](../server/VolumeService.md)

`AuthorizeExpression` defaults to `#deny`.

`AuthorizeExpression` is queried through [UnityAccessDecorator](UnityAccessDecorator.md#findAuthorizeExpression).
