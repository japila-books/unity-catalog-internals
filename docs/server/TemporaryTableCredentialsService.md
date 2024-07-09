# TemporaryTableCredentialsService

`TemporaryTableCredentialsService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/temporary-table-credentials` URL.

Method | URL | Handler | Params
-|-|-|-
 POST | | [generateTemporaryTableCredential](#generateTemporaryTableCredential) | [GenerateTemporaryTableCredential](GenerateTemporaryTableCredential.md)

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
