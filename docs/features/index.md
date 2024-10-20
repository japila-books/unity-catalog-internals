# {{ book.title }}

**Unity Catalog** is an [open-source universal catalog](https://www.unitycatalog.io/) of the following assets:

* [Catalogs](../server/CatalogService.md)
* Credentials (for [Tables](../server/TemporaryTableCredentialsService.md) and [Volumes](../server/TemporaryVolumeCredentialsService.md))
* [Functions](../server/FunctionService.md)
* [Models](../server/ModelService.md)
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

## Learning Resources

1. [Open Sourcing Unity Catalog](https://www.databricks.com/blog/open-sourcing-unity-catalog)
1. [Getting Started with X-Table and Unity Catalog | Universal Datalakes | Hands on Labs](https://www.linkedin.com/pulse/getting-started-x-table-unity-catalog-universal-datalakes-soumil-shah-l3rpe/) with an accompanying [video on YouTube](https://youtu.be/1SKQRrenBj4)
1. [Unitycatalog: the first look](https://semyonsinchenko.github.io/ssinchenko/post/uniticatalog-first-look/)
