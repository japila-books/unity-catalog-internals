# Spark Connector

**Spark Connector** allows Apache Spark to use Unity Catalog as a metastore.

The following features are supported:

* Read/write (partitioned) external parquet tables
* Read/write (partitioned) external delta tables
* Support the path table syntax of delta tables
* [Temporary credentials for secured access](./UCProxy.md#loadTable) to local and S3 tables ([parquet tables only, no delta tables yet]({{ uc.commit }}/681acbdb46f375d00e402739bc3ea31fc407e732))
* [Namespace](#namespace-support)

Spark Connector supports Delta Lake, Iceberg and Hudi tables via [UniForm]({{ book.delta }}/uniform/).

!!! note "No Native Iceberg Table Support"
    There is no native Iceberg table support. It is slated for v0.3 or v0.4 per the [Proposed UC Roadmap CY2024Q4](https://github.com/unitycatalog/unitycatalog/discussions/411).

Spark Connector is [UCSingleCatalog](UCSingleCatalog.md) and [UCProxy](UCProxy.md).

## Spark and Java Compatibility

Apache Spark {{ spark.version }} and Java 11 are used to build Spark Connector module for better Apache Spark interoperability (see [this commit]({{ uc.commit }}/d2fbca32cd0068fabe0d2e7f0fb277ba892a6be3)).

## Namespace Support

As of [this commit]({{ uc.commit }}/10c57d14d2af5e208f6e15f06df4950b6d587ba1), Unity Catalog supports various namespace-related commands (e.g., `SHOW NAMESPACES`, `DESC NAMESPACE`).

See [this demo](../demo/namespace-support-in-spark-connector.md) to learn more.

## Demo

[Demo: Spark Connector](../demo/spark-connector.md)
