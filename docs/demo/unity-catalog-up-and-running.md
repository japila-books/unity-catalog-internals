---
hide:
- navigation
---

# Demo: Unity Catalog Up and Running

## Install Java 17

Java 17 or above is required to start Unity Catalog's [server](../server/index.md) and [CLI](../cli/index.md).

```text
$ java --version
openjdk 17.0.18 2026-01-20 LTS
OpenJDK Runtime Environment Zulu17.64+15-CA (build 17.0.18+8-LTS)
OpenJDK 64-Bit Server VM Zulu17.64+15-CA (build 17.0.18+8-LTS, mixed mode, sharing)
```

## Start UC Server

```shell
./bin/start-uc-server
```

## List Tables

Open a separate terminal.

Execute the following command:

```shell
./bin/uc table list --catalog unity --schema default
```

```console
$ ./bin/uc table list --catalog unity --schema default --output json | jq ".[].name"
"marksheet"
"marksheet_uniform"
"numbers"
"user_countries"
```

## Describe (Get) Table

### Managed Table

```console
$ ./bin/uc table get --full_name unity.default.marksheet --output jsonPretty
{
  "name" : "marksheet",
  "catalog_name" : "unity",
  "schema_name" : "default",
  "table_type" : "MANAGED",
  "data_source_format" : "DELTA",
  "columns" : [ {
  ...
  } ],
  "storage_location" : "file:///Users/jacek/oss/unitycatalog/etc/data/managed/unity/default/tables/marksheet",
  "comment" : "Managed table",
  "properties" : {
    "key1" : "value1",
    "key2" : "value2"
  },
  "owner" : null,
  "created_at" : 1721234405595,
  "created_by" : null,
  "updated_at" : 1721234405595,
  "updated_by" : null,
  "table_id" : "c389adfa-5c8f-497b-8f70-26c2cca4976d"
}
```

### External Table

!!! warning "Work in progress"

```console
❯ ./bin/uc table get --full_name unity.default.test_table --output jsonPretty
{
  "name" : "test_table",
  "catalog_name" : "unity",
  "schema_name" : "default",
  "table_type" : "EXTERNAL",
  "data_source_format" : "DELTA",
  "columns" : [ ],
  "storage_location" : "s3://uc-japila/raw/test_table",
  "comment" : null,
  "properties" : { },
  "owner" : null,
  "created_at" : 1729282596872,
  "created_by" : null,
  "updated_at" : 1729282596872,
  "updated_by" : null,
  "table_id" : "37b15062-cd84-42c3-8b38-ee1e724f74c7"
}
```
