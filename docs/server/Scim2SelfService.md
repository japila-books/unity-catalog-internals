# Scim2SelfService

`Scim2SelfService` is a SCIM2-compliant `/Me` endpoint.

`Scim2SelfService` is an API service of [UnityCatalogServer](UnityCatalogServer.md) to handle HTTP requests at `/api/1.0/unity-control/scim2/Me` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | - | [getCurrentUser](#getCurrentUser) | -

```console
# 🛑 Start the UC server with server authorization enabled
$ http http://localhost:8080/api/1.0/unity-control/scim2/Me
HTTP/1.1 401 Unauthorized
content-length: 173
content-type: application/json
date: Tue, 17 Dec 2024 21:23:01 GMT
server: Armeria/1.28.4

{
    "details": [
        {
            "@type": "google.rpc.ErrorInfo",
            "metadata": {},
            "reason": "UNAUTHENTICATED"
        }
    ],
    "error_code": "UNAUTHENTICATED",
    "message": "No authorization found.",
    "stack_trace": null
}
```

```console
$ http -A bearer -a $(cat etc/conf/token.txt) \
    http://localhost:8080/api/1.0/unity-control/scim2/Me
HTTP/1.1 200 OK
content-length: 345
content-type: application/scim+json
date: Tue, 17 Dec 2024 21:23:29 GMT
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
        "lastModified": "2024-12-17T21:23:29.251+00:00",
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

## Creating Instance

`Scim2SelfService` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](../server-authorization/UnityCatalogAuthorizer.md)

`Scim2SelfService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## UserRepository { #USER_REPOSITORY }

`Scim2SelfService` looks up the system-wide [UserRepository](../persistent-storage/UserRepository.md#getInstance) when [created](#creating-instance).

## Get Current User { #getCurrentUser }

```java
UserResource getCurrentUser()
```

`getCurrentUser` finds a [JSON web token](../server-authorization/AuthDecorator.md#DECODED_JWT_ATTR) in the server-side request context.

`getCurrentUser` uses the `sub` claim (of the decoded JSON web token) as the email of a user to look up.

`getCurrentUser` requests the system-wide [UserRepository](#USER_REPOSITORY) instance to [look up a user by the email](../persistent-storage/UserRepository.md#getUserByEmail).

??? note "Scim2RuntimeException"
    `getCurrentUser` reports a `Scim2RuntimeException` when there is no [JSON web token](../server-authorization/AuthDecorator.md#DECODED_JWT_ATTR) in the server-side request context:

    ```text
    No user found.
    ```
