# CatalogService

`CatalogService` is a Unity Catalog API service that [UnityCatalogServer](UnityCatalogServer.md) uses to handle HTTP requests at `/api/2.1/unity-catalog/catalogs` URL.

Method | URL | Handler | Params
-|-|-|-
 GET | | [listCatalogs](#listCatalogs) |
 POST | | [createCatalog](#createCatalog) | JSON-ified [CreateCatalog](CreateCatalog.md)
 GET | `/{name}` | [getCatalog](#getCatalog) | <ul><li>name</li></ul>
 PATCH | `/{name}` | [updateCatalog](#updateCatalog) | <ul><li>name</li></ul>
 DELETE | `/{name}` | [deleteCatalog](#deleteCatalog) | <ul><li>name</li></ul>

```console
$ http http://localhost:8081/api/2.1/unity-catalog/catalogs
HTTP/1.1 200 OK
content-length: 184
content-type: application/json
date: Thu, 4 Jul 2024 17:56:19 GMT
server: Armeria/1.28.4

{
    "catalogs": [
        {
            "comment": "Main catalog",
            "created_at": 1720090500565,
            "id": "17562adb-e6f8-463e-b82a-22264b067d6b",
            "name": "unity",
            "properties": {},
            "updated_at": null
        }
    ],
    "next_page_token": null
}
```

```console
$ http http://localhost:8081/api/2.1/unity-catalog/catalogs | jq '.catalogs[].name'
"unity"
```
