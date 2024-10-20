---
hide:
- navigation
---

# Demo: Unity Catalog Up and Running

## Install Java 17

Java 17 or above is required to start Unity Catalog's [server](../server/index.md) and [CLI](../cli/index.md).

```text
$ java --version
openjdk 17.0.12 2024-07-16 LTS
OpenJDK Runtime Environment Zulu17.52+17-CA (build 17.0.12+7-LTS)
OpenJDK 64-Bit Server VM Zulu17.52+17-CA (build 17.0.12+7-LTS, mixed mode, sharing)
```

## Start UC Server

```text
❯ ./bin/start-uc-server
###################################################################
#  _    _       _ _            _____      _        _              #
# | |  | |     (_) |          / ____|    | |      | |             #
# | |  | |_ __  _| |_ _   _  | |     __ _| |_ __ _| | ___   __ _  #
# | |  | | '_ \| | __| | | | | |    / _` | __/ _` | |/ _ \ / _` | #
# | |__| | | | | | |_| |_| | | |___| (_| | || (_| | | (_) | (_| | #
#  \____/|_| |_|_|\__|\__, |  \_____\__,_|\__\__,_|_|\___/ \__, | #
#                      __/ |                                __/ | #
#                     |___/               v{{ uc.version }}  |___/  #
###################################################################
```

## Start UC CLI

```text
❯ ./bin/uc
Please provide a entity.

Usage: bin/uc <entity> <operation> [options]
Entities: schema, volume, model_version, metastore, auth, catalog, function, permission, registered_model, user, table

By default, the client will connect to UC running locally at http://localhost:8080

To connect to specific UC server, use --server https://<host>:<port>

Currently, auth using bearer token is supported. Please specify the token via --auth_token <PAT Token>

For detailed help on entity specific operations, use bin/uc <entity> --help
```

## List Tables

```text
$ ./bin/uc table list --catalog unity --schema default
┌─────────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────┬────────────────────────────────────┐
│      NAME       │CATALOG_NAME│SCHEMA_NAME │ TABLE_TYPE │DATA_SOURCE_│  COLUMNS   │STORAGE_LOCA│  COMMENT   │ PROPERTIES │ CREATED_AT │ UPDATED_AT │              TABLE_ID              │
│                 │            │            │            │   FORMAT   │            │    TION    │            │            │            │            │                                    │
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│marksheet        │unity       │default     │MANAGED     │DELTA       │[{"name":...│file:///U...│Managed t...│{"key1":"...│172123440...│172123440...│c389adfa-5c8f-497b-8f70-26c2cca4976d│
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│marksheet_uniform│unity       │default     │EXTERNAL    │DELTA       │[{"name":...│file:///t...│Uniform t...│{"key1":"...│172123440...│172123440...│9a73eb46-adf0-4457-9bd8-9ab491865e0d│
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│numbers          │unity       │default     │EXTERNAL    │DELTA       │[{"name":...│file:///U...│External ...│{"key1":"...│172123440...│172123440...│32025924-be53-4d67-ac39-501a86046c01│
├─────────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼────────────────────────────────────┤
│user_countries   │unity       │default     │EXTERNAL    │DELTA       │[{"name":...│file:///U...│Partition...│{}          │172123440...│172123440...│26ed93b5-9a18-4726-8ae8-c89dfcfea069│
└─────────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴────────────────────────────────────┘
```

```console
❯ ./bin/uc table list --catalog unity --schema default --output json | jq ".[].name"
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
  "storage_location" : "file:///Users/jacek/dev/oss/unitycatalog/etc/data/managed/unity/default/tables/marksheet/",
  "comment" : "Managed table",
  "properties" : {
    "key1" : "value1",
    "key2" : "value2"
  },
  "created_at" : 1721234405595,
  "updated_at" : 1721234405595,
  "table_id" : "c389adfa-5c8f-497b-8f70-26c2cca4976d"
}
```

### External Table

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
