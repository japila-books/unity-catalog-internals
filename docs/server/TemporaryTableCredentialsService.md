# TemporaryTableCredentialsService

`TemporaryTableCredentialsService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/temporary-table-credentials` URL.

Method | URL | Handler | Params
-|-|-|-
 POST | | [generateTemporaryTableCredential](#generateTemporaryTableCredential) | [GenerateTemporaryTableCredential](GenerateTemporaryTableCredential.md)

## Creating Instance

`TemporaryTableCredentialsService` takes the following to be created:

* <span id="credentialOps"> [CredentialOperations](CredentialOperations.md)

`TemporaryTableCredentialsService` is created when:

* `UnityCatalogServer` is requested to [register the API services](UnityCatalogServer.md#addServices)

## TableRepository { #TABLE_REPOSITORY }

`TemporaryTableCredentialsService` looks up the system-wide [TableRepository](../persistent-storage/TableRepository.md#getInstance) instance when created.

## Looking Up Table Credentials { #generateTemporaryTableCredential }

```java
HttpResponse generateTemporaryTableCredential(
  GenerateTemporaryTableCredential generateTemporaryTableCredential)
```

`generateTemporaryTableCredential` [looks up the table metadata](../persistent-storage/TableRepository.md#getTableById) (by the `tableId` of the given `GenerateTemporaryTableCredential`) in the [TableRepository](#TABLE_REPOSITORY).

Unless the storage location is on S3 (starts with `s3://` prefix), `generateTemporaryTableCredential` assumes local file system and returns empty credentials.

For a S3 storage location, `generateTemporaryTableCredential` [finds the S3 storage location credentials](TemporaryCredentialUtils.md#findS3BucketConfig).

## Demo

### Local File System

```console
$ http http://localhost:8081/api/2.1/unity-catalog/temporary-table-credentials \
    table_id=b5d6db68-5eca-485c-be5f-5f53d4f27f60 \
    operation=READ
HTTP/1.1 200 OK
content-length: 52
content-type: application/json
date: Tue, 9 Jul 2024 11:54:58 GMT
server: Armeria/1.28.4

{
    "aws_temp_credentials": null,
    "expiration_time": null
}
```

### S3 Storage Location

Register a table on S3.

```console
$ ./bin/uc table create \
    --full_name unity.default.s3_creds_demo \
    --columns "id INT, name STRING" \
    --storage_location "s3://japila.pl/my_demo_bucket/s3_creds_demo"
┌────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        KEY         │                                               VALUE                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                │s3_creds_demo                                                                                       │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME        │unity                                                                                               │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME         │default                                                                                             │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_TYPE          │EXTERNAL                                                                                            │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_SOURCE_FORMAT  │DELTA                                                                                               │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COLUMNS             │{"name":"id","type_text":"int","type_json":"{\"name\":\"id\",\"type\":\"integer\",\"nullable\":true,│
│                    │\"metadata\":{}}","type_name":"INT","type_precision":0,"type_scale":0,"type_interval_type":null,"pos│
│                    │ition":0,"comment":null,"nullable":true,"partition_index":null}                                     │
│                    │{"name":"name","type_text":"string","type_json":"{\"name\":\"name\",\"type\":\"string\",\"nullable\"│
│                    │:true,\"metadata\":{}}","type_name":"STRING","type_precision":0,"type_scale":0,"type_interval_type":│
│                    │null,"position":1,"comment":null,"nullable":true,"partition_index":null}                            │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│STORAGE_LOCATION    │s3://japila.pl/my_demo_bucket/s3_creds_demo                                                         │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT             │null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES          │{}                                                                                                  │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT          │1720539043045                                                                                       │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT          │null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│TABLE_ID            │020270b2-621e-4157-a73d-6a63c3b86bdd                                                                │
└────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```console
$ http http://localhost:8081/api/2.1/unity-catalog/temporary-table-credentials \
    table_id=020270b2-621e-4157-a73d-6a63c3b86bdd   \
    operation=READ

HTTP/1.1 400 Bad Request
content-length: 192
content-type: application/json
date: Tue, 9 Jul 2024 14:54:48 GMT
server: Armeria/1.28.4

{
    "details": [
        {
            "@type": "google.rpc.ErrorInfo",
            "metadata": {},
            "reason": "FAILED_PRECONDITION"
        }
    ],
    "error_code": "FAILED_PRECONDITION",
    "message": "S3 bucket configuration not found.",
    "stack_trace": null
}
```

Add a S3 bucket configuration to `etc/conf/server.properties` for the table location and bounce the UC server.

```console
$ cat etc/conf/server.properties
server.env=dev
## temp credential config for s3 (Multiple s3 config can be added by incrementing the index)
s3.bucketPath.0=s3://japila.pl
s3.accessKey.0=FIXME_accessKey
s3.secretKey.0=FIXME_secretKey
s3.sessionToken.0=FIXME_sessionToken
```

```console
./bin/start-uc-server
```

```console
$ http http://localhost:8081/api/2.1/unity-catalog/temporary-table-credentials \
    table_id=020270b2-621e-4157-a73d-6a63c3b86bdd   \
    operation=READ
HTTP/1.1 200 OK
content-length: 158
content-type: application/json
date: Tue, 9 Jul 2024 15:32:04 GMT
server: Armeria/1.28.4

{
    "aws_temp_credentials": {
        "access_key_id": "FIXME_accessKey",
        "secret_access_key": "FIXME_secretKey",
        "session_token": "FIXME_sessionToken"
    },
    "expiration_time": null
}
```
