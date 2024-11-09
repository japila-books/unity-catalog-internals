# PermissionService

`PermissionService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/permissions` URL.

Method | URL | Handler | SecurableType
-|-|-|-
 GET | `/catalog/{name}` | [getCatalogAuthorization](#getCatalogAuthorization) | `catalog`
 GET | `/function/{name}` | [getFunctionAuthorization](#getFunctionAuthorization) | `function`
 GET | `/metastore/{name}` | [getMetastoreAuthorization](#getMetastoreAuthorization) | `metastore`
 GET | `/registered_model/{name}` | [getRegisteredModelAuthorization](#getRegisteredModelAuthorization) | `registered_model`
 GET | `/schema/{name}` | [getSchemaAuthorization](#getSchemaAuthorization) | `schema`
 GET | `/table/{name}` | [getTableAuthorization](#getTableAuthorization) | `table`
 GET | `/volume/{name}` | [getVolumeAuthorization](#getVolumeAuthorization) | `volume`

Method | URL | Handler | AuthorizeKey
-|-|-|-
 PATCH | `/metastore/{name}` | [updateMetastoreAuthorization](#updateMetastoreAuthorization) | `metastore`
 ... | | |

``` console
$ http http://localhost:8081/api/2.1/unity-catalog/permissions/catalog/unity
HTTP/1.1 200 OK
content-length: 28
content-type: application/json
date: Thu, 3 Oct 2024 15:30:28 GMT
server: Armeria/1.28.4

{
    "privilege_assignments": []
}
```

??? note "Unity Catalog CLI"
    The above `http` command is equivalent to the following:

    ``` console
    ❯ ./bin/uc permission get --securable_type catalog --name unity
    []
    ```

## Creating Instance

`PermissionService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)

`PermissionService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## Get Authorization { #getAuthorization }

```java
HttpResponse getAuthorization(
  SecurableType securableType,
  String name)
```

`getAuthorization` [finds the ID](#getResourceId) of the given `SecurableType` and `name`.

`getAuthorization` [finds the ID of the current principal](../server-authorization/IdentityUtils.md#findPrincipalId).

`getAuthorization`...FIXME

---

`getAuthorization` is used when `PermissionService` is requested for the following authorizations:

* [Catalog](#getCatalogAuthorization)
* [Function](#getFunctionAuthorization)
* [Metastore](#getMetastoreAuthorization)
* [RegisteredModel](#getRegisteredModelAuthorization)
* [Schema](#getSchemaAuthorization)
* [Table](#getTableAuthorization)
* [Volume](#getVolumeAuthorization)

## Update Authorization { #updateAuthorization }

```java
HttpResponse updateAuthorization(
  SecurableType securableType,
  String name,
  UpdatePermissions request)
```

`updateAuthorization`...FIXME

## Get Metastore Authorization { #getMetastoreAuthorization }

```java
HttpResponse getMetastoreAuthorization(
  String name)
```

`getMetastoreAuthorization` [getAuthorization](#getAuthorization) of the `METASTORE` securable type with the given `name`.

---

`getMetastoreAuthorization` is used to handle `GET /metastore/{name}` requests.
