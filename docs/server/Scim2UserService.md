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

## UserRepository { #USER_REPOSITORY }

`Scim2UserService` looks up the system-wide [UserRepository](../persistent-storage/UserRepository.md) when created.

## Creating Instance

`Scim2UserService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)

`Scim2UserService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## getCurrentUser { #getCurrentUser }

```java
UserResource getCurrentUser()
```

??? note "Authorization"
    `getCurrentUser` handles `POST` requests with the following:

    * [AuthorizeExpression](../server-authorization/AuthorizeExpression.md): `#principal != null`
    * [AuthorizeKey](../server-authorization/AuthorizeKey.md): `METASTORE`

`getCurrentUser` finds a [JSON web token](../server-authorization/AuthDecorator.md#DECODED_JWT_ATTR) in the server-side request context.

`getCurrentUser` returns the [getUserByEmail](../persistent-storage/UserRepository.md#getUserByEmail) (from the system-wide [UserRepository](#USER_REPOSITORY)) for the `sub` claim of the decoded JSON web token.

??? note "Scim2RuntimeException for no JSON web token"
    `getCurrentUser` reports a `Scim2RuntimeException` when there is no [JSON web token](../server-authorization/AuthDecorator.md#DECODED_JWT_ATTR) in the server-side request context:

    ```text
    No user found.
    ```

## Examples

### Get All Users

```console
$ https -A bearer -a $(cat etc/conf/token.txt) \
    http://localhost:8080/api/1.0/unity-control/scim2/Users
HTTP/1.1 200 OK
content-length: 595
content-type: application/scim+json
date: Sat, 9 Nov 2024 12:37:44 GMT
server: Armeria/1.28.4

{
    "Resources": [
        {
            "active": true,
            "displayName": "Admin",
            "emails": [
                {
                    "primary": true,
                    "value": "admin"
                }
            ],
            "id": "cd941442-6635-45b9-bc7a-c9b527600b3b",
            "meta": {
                "created": "2024-11-08T18:40:16.216+01:00",
                "lastModified": "2024-11-09T13:37:44.636+01:00",
                "resourceType": "User"
            },
            "photos": [
                {
                    "value": ""
                }
            ],
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:User"
            ],
            "userName": "admin"
        }
    ],
    "itemsPerPage": 1,
    "meta": {
        "created": "2024-11-09T12:37:44.636+00:00",
        "lastModified": "2024-11-09T12:37:44.636+00:00",
        "resourceType": "User"
    },
    "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ],
    "startIndex": 1,
    "totalResults": 1
}
```

### Get User by ID

```console
$ https -A bearer -a $(cat etc/conf/token.txt) \
    http://localhost:8080/api/1.0/unity-control/scim2/Users/cd941442-6635-45b9-bc7a-c9b527600b3b
HTTP/1.1 200 OK
content-length: 345
content-type: application/scim+json
date: Sat, 9 Nov 2024 12:41:36 GMT
server: Armeria/1.28.4

{
    "active": true,
    "displayName": "Admin",
    "emails": [
        {
            "primary": true,
            "value": "admin"
        }
    ],
    "id": "cd941442-6635-45b9-bc7a-c9b527600b3b",
    "meta": {
        "created": "2024-11-08T17:40:16.216+00:00",
        "lastModified": "2024-11-09T12:41:36.534+00:00",
        "resourceType": "User"
    },
    "photos": [
        {
            "value": ""
        }
    ],
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "userName": "admin"
}
```

### Get Current User

```console
$ https -A bearer -a $(cat etc/conf/token.txt) \
    http://localhost:8080/api/1.0/unity-control/scim2/Users/self
HTTP/1.1 200 OK
content-length: 345
content-type: application/scim+json
date: Sat, 9 Nov 2024 12:35:40 GMT
server: Armeria/1.28.4

{
    "active": true,
    "displayName": "Admin",
    "emails": [
        {
            "primary": true,
            "value": "admin"
        }
    ],
    "id": "cd941442-6635-45b9-bc7a-c9b527600b3b",
    "meta": {
        "created": "2024-11-08T17:40:16.216+00:00",
        "lastModified": "2024-11-09T12:35:40.341+00:00",
        "resourceType": "User"
    },
    "photos": [
        {
            "value": ""
        }
    ],
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "userName": "admin"
}
```
