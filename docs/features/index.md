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

## Running Unity Catalog

Java 17 or above is required to build and run Unity Catalog.

```text
$ java --version
openjdk 17.0.11 2024-04-16 LTS
OpenJDK Runtime Environment Zulu17.50+19-CA (build 17.0.11+9-LTS)
OpenJDK 64-Bit Server VM Zulu17.50+19-CA (build 17.0.11+9-LTS, mixed mode, sharing)
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
#                     |___/               v0.1.0-SNAPSHOT  |___/  #
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

## Learning Resources

1. [Open Sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog)
1. [Getting Started with X-Table and Unity Catalog | Universal Datalakes | Hands on Labs](https://www.linkedin.com/pulse/getting-started-x-table-unity-catalog-universal-datalakes-soumil-shah-l3rpe/) with an accompanying [video on YouTube](https://youtu.be/1SKQRrenBj4)
1. [Unitycatalog: the first look](https://semyonsinchenko.github.io/ssinchenko/post/uniticatalog-first-look/)
