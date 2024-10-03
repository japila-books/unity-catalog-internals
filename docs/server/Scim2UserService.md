# Scim2UserService

`Scim2UserService` is a SCIM2-compliant user management service.

`Scim2UserService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle `/api/1.0/unity-control/scim2/Users` endpoint.

Method | URL | Handler | Params
-|-|-|-
 GET | `/` | [getScimUsers](#getScimUsers) | <ul><li>filter<li>startIndex<li>count</ul>
 POST | `/` | [createScimUser](#createScimUser) | JSON-ified `UserResource`
 GET | `/self` | [getCurrentUser](#getCurrentUser) | -
 GET | `/{id}` | [getUser](#getUser) | <ul><li>id</ul>
 PUT | `/{id}` | [updateUser](#updateUser) | <ul><li>id<li>JSON-ified `UserResource`</ul>
 DELETE | `/{id}` | [deleteUser](#deleteUser) | <ul><li>id</ul>

``` console
$ http http://localhost:8081/api/1.0/unity-control/scim2/Users
HTTP/1.1 200 OK
content-length: 250
content-type: application/scim+json
date: Tue, 24 Sep 2024 20:38:44 GMT
server: Armeria/1.28.4

{
    "Resources": [],
    "itemsPerPage": 0,
    "meta": {
        "created": "2024-09-24T20:38:44.665+00:00",
        "lastModified": "2024-09-24T20:38:44.665+00:00",
        "resourceType": "User"
    },
    "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ],
    "startIndex": 1,
    "totalResults": 0
}
```

## UserRepository { #USER_REPOSITORY }

`Scim2UserService` looks up the system-wide [UserRepository](../persistent-storage/UserRepository.md) when created.

## Creating Instance

`Scim2UserService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)

`Scim2UserService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)
