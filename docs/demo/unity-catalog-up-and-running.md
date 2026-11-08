---
hide:
- navigation
---

# Demo: Unity Catalog Up and Running

## Install Java 17

Java 17 or above is required to start Unity Catalog's [server](../server/index.md) and [CLI](../cli/index.md).

```text
$ java --version
openjdk 17.0.21 2026-10-20 LTS
OpenJDK Runtime Environment Zulu17.70+111-CA (build 17.0.21+9-LTS)
OpenJDK 64-Bit Server VM Zulu17.70+111-CA (build 17.0.21+9-LTS, mixed mode, sharing)
```

## Start Unity Catalog Server

```shell
./bin/start-uc-server
```

## List Tables

Open a separate terminal.

Execute the following command:

```shell
./bin/uc table list --catalog unity --schema default --output jsonPretty | jq '[.[] | {name, table_type}]'
```

```json
[
  {
    "name": "marksheet",
    "table_type": "MANAGED"
  },
  {
    "name": "marksheet_uniform",
    "table_type": "EXTERNAL"
  },
  {
    "name": "numbers",
    "table_type": "EXTERNAL"
  },
  {
    "name": "user_countries",
    "table_type": "EXTERNAL"
  }
]
```

## Describe (Get) Table

### Managed Table

```shell
./bin/uc table get --full_name unity.default.marksheet --output jsonPretty | jq '.columns = [] | del(..|nulls)'
```

```json
{
  "name": "marksheet",
  "catalog_name": "unity",
  "schema_name": "default",
  "table_type": "MANAGED",
  "data_source_format": "DELTA",
  "columns": [],
  "storage_location": "file:///Users/jacek/oss/unitycatalog/etc/data/managed/unity/default/tables/marksheet",
  "comment": "Managed table",
  "properties": {
    "key1": "value1",
    "key2": "value2"
  },
  "created_at": 1721234405595,
  "updated_at": 1721234405595,
  "table_id": "c389adfa-5c8f-497b-8f70-26c2cca4976d"
}
```

### External Table

```shell
./bin/uc table get --full_name unity.default.user_countries --output jsonPretty | jq '.columns = [] | del(..|nulls)'
```

```json
{
  "name": "user_countries",
  "catalog_name": "unity",
  "schema_name": "default",
  "table_type": "EXTERNAL",
  "data_source_format": "DELTA",
  "columns": [],
  "storage_location": "file:///Users/jacek/oss/unitycatalog/etc/data/external/unity/default/tables/user_countries",
  "comment": "Partitioned table",
  "properties": {},
  "created_at": 1721234405622,
  "updated_at": 1721234405622,
  "table_id": "26ed93b5-9a18-4726-8ae8-c89dfcfea069"
}
```
