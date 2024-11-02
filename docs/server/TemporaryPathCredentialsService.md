# TemporaryPathCredentialsService

`TemporaryPathCredentialsService` is an API service of [UnityCatalogServer](UnityCatalogServer.md) to handle HTTP requests at `/api/2.1/unity-catalog/temporary-path-credentials` URL.

Method | URL | Handler | Params
-|-|-|-
 POST | `/` | [generateTemporaryPathCredential](#generateTemporaryPathCredential) | JSON-ified `GenerateTemporaryPathCredential`

`TemporaryPathCredentialsService` handles `POST` requests only with the following authorization guarantees:

Method | AuthorizeExpression | Securables
-|-|-
 POST | [authorize(#principal, #metastore, OWNER)](../server-authorization/AuthorizeExpression.md) | [METASTORE](../basic-server-access-control/index.md#securables)

## Demo

!!! note "etc/conf/server.properties"
    The following demo requires `url` being configured in [etc/conf/server.properties](index.md#server-configuration) (using`s3.bucketPath.0=s3://uc-japila` and the others).

```console
$ http http://localhost:8081/api/2.1/unity-catalog/temporary-path-credentials \
    url=s3://uc-japila \
    operation=PATH_CREATE_TABLE
HTTP/1.1 200 OK
content-length: 1198
content-type: application/json
date: Sat, 2 Nov 2024 19:51:29 GMT
server: Armeria/1.28.4

{
    "aws_temp_credentials": {
        "access_key_id": "xxx",
        "secret_access_key": "xxx",
        "session_token": "xxx"
    },
    "azure_user_delegation_sas": null,
    "expiration_time": null,
    "gcp_oauth_token": null
}
```

## Creating Instance

`TemporaryPathCredentialsService` takes the following to be created:

* <span id="credentialOps"> [CredentialOperations](../credential-vending/CredentialOperations.md)

`TemporaryPathCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## Generate Temporary Path Credentials { #generateTemporaryPathCredential }

``` java
HttpResponse generateTemporaryPathCredential(
  GenerateTemporaryPathCredential generateTemporaryPathCredential)
```

`generateTemporaryPathCredential` requests this [CredentialOperations](#credentialOps) to [vendCredential](../credential-vending/CredentialOperations.md#vendCredential) for the `url` and `operation` properties (of the given `GenerateTemporaryPathCredential`).

!!! note "Internal Server Error"
    `operation` should be one of the [supported path operations](../credential-vending/index.md#path-operations) or Unity Catalog reports an internal error.

### Privileges by Path Operation { #pathOperationToPrivileges }

```java
Set<CredentialContext.Privilege> pathOperationToPrivileges(
  PathOperation pathOperation)
```

`pathOperationToPrivileges` converts the given [PathOperation](../credential-vending/index.md#path-operations) to [Privileges](../basic-server-access-control/index.md#privileges):

PathOperation | Privileges
-|-
 `PATH_READ` | `SELECT`
 `PATH_READ_WRITE` | `SELECT` and `UPDATE`
 `PATH_CREATE_TABLE` | `SELECT` and `UPDATE`
 `UNKNOWN_PATH_OPERATION` | (empty)
