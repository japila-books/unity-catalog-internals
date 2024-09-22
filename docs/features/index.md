# {{ book.title }}

**Unity Catalog** is an [open-source universal catalog](https://www.unitycatalog.io/) of the following assets:

* [Catalogs](../server/CatalogService.md)
* Credentials (for [Tables](../server/TemporaryTableCredentialsService.md) and [Volumes](../server/TemporaryVolumeCredentialsService.md))
* [Functions](../server/FunctionService.md)
* [Schemas](../server/SchemaService.md)
* [Tables](../server/TableService.md)
* [Volumes](../server/VolumeService.md)

Unity Catalog is made up of the following runtimes:

* [Reference Server](../server/index.md)
* [Example CLI](../cli/index.md) (based on the [Client API](../client/index.md))

The server and CLI can be started on command line using `bin/start-uc-server` and `bin/uc` shell scripts, respectively.

## Different Kinds of Catalogs

As [Jason Reid posted](https://unitycatalog.slack.com/archives/C076YREKX8W/p1723847215055299?thread_ts=1723739789.081249&cid=C076YREKX8W) on the **unity-catalog** slack channel (quoted with some styling changes):

> First, a bit of clarification on the term "catalog" which is unfortunately overloaded. It is common to differentiate between so-called "business catalogs" and "operational catalogs".
>
> **Operational catalogs** are what query engines use to read and write data. They track table schema and state and are often involved in transaction management.
>
> Examples: Hive Metastore, **Unity Catalog**, AWS Glue, Polaris
>
> **Business catalogs** are designed primarily for discovery. They typically aggregate metadata from a wide variety of data systems and make it easy to search.
>
> Examples: Atlan, DataHub, Alation
>
> For security, that is typically enforced by a combination of an operational catalog (where policy is defined) and the query engine (where policy is enforced).
>
> There are some solutions for policy management which can push policy into multiple systems.
>
> Examples: Immuta, Privacera

## Running Unity Catalog

Java 17 or above is required to build and run Unity Catalog.

```text
$ java --version
openjdk 17.0.12 2024-07-16 LTS
OpenJDK Runtime Environment Zulu17.52+17-CA (build 17.0.12+7-LTS)
OpenJDK 64-Bit Server VM Zulu17.52+17-CA (build 17.0.12+7-LTS, mixed mode, sharing)
```

```text
$ ./bin/start-uc-server
###################################################################
#  _    _       _ _            _____      _        _              #
# | |  | |     (_) |          / ____|    | |      | |             #
# | |  | |_ __  _| |_ _   _  | |     __ _| |_ __ _| | ___   __ _  #
# | |  | | '_ \| | __| | | | | |    / _` | __/ _` | |/ _ \ / _` | #
# | |__| | | | | | |_| |_| | | |___| (_| | || (_| | | (_) | (_| | #
#  \____/|_| |_|_|\__|\__, |  \_____\__,_|\__\__,_|_|\___/ \__, | #
#                      __/ |                                __/ | #
#                     |___/               v0.2.0-SNAPSHOT  |___/  #
###################################################################
```

```text
$ ./bin/uc
Please provide a entity.

Usage: bin/uc <entity> <operation> [options]
Entities: schema, volume, catalog, function, table

By default, the client will connect to UC running locally at http://localhost:8080

To connect to specific UC server, use --server https://<host>

Currently, auth using bearer token is supported. Please specify the token via --auth_token <PAT Token>

For detailed help on entity specific operations, use bin/uc <entity> --help
```

```console
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

## Learning Resources

1. [Open Sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog)
1. [Getting Started with X-Table and Unity Catalog | Universal Datalakes | Hands on Labs](https://www.linkedin.com/pulse/getting-started-x-table-unity-catalog-universal-datalakes-soumil-shah-l3rpe/) with an accompanying [video on YouTube](https://youtu.be/1SKQRrenBj4)
1. [Unitycatalog: the first look](https://semyonsinchenko.github.io/ssinchenko/post/uniticatalog-first-look/)
