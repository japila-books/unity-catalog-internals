---
hide:
- navigation
---

# Demo: Full Apache Iceberg Table Support

Unity Catalog 0.7.0 extends its support for Iceberg tables with Iceberg REST catalog APIs for table operations. Now, any engine that supports the Apache Iceberg REST protocol can create, write to, read from, rename, and drop Iceberg tables in Unity Catalog.

!!! warning "Apache Iceberg and Apache Spark Compatibility"
    The latest version of [Apache Iceberg 1.12.0](https://iceberg.apache.org/releases/) supports up to and including [Apache Spark 4.1](https://spark.apache.org/news/spark-4-1-4-released.html).

```shell
./bin/spark-shell --version
```

```text
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 4.1.4
      /_/

Using Scala version 2.13.17, OpenJDK 64-Bit Server VM, 17.0.21
Branch HEAD
Compiled by user root on 2026-10-22T05:35:32Z
Revision 45b9b176e6e27f530a86ac5421b03865b7ea6287
```

## Start Unity Catalog Server

```shell
./bin/start-uc-server
```

## Create Catalog in Unity Catalog for Iceberg Tables

```shell
./bin/uc catalog create --name unity_iceberg --storage_root "file:///tmp/uc-storage-root/"
```

```shell
./bin/uc catalog list --output jsonPretty | jq '[.[] | del(..|nulls)]'
```

```json
[
  {
    "name": "unity_iceberg",
    "properties": {},
    "created_at": 1794163724305,
    "updated_at": 1794163724305,
    "id": "c1bf40a0-6348-4cee-a3b0-c59229a288b3",
    "storage_root": "file:///tmp/uc-storage-root",
    "storage_location": "file:///tmp/uc-storage-root/__unitystorage/catalogs/c1bf40a0-6348-4cee-a3b0-c59229a288b3"
  },
  ...
]
```

## Start Spark SQL

!!! warning "Use Apache Spark 4.1"

```shell
./bin/spark-sql \
   --packages org.apache.iceberg:iceberg-spark-runtime-4.1_2.13:1.12.0 \
   --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
   --conf spark.sql.catalog.unity_iceberg=org.apache.iceberg.spark.SparkCatalog \
   --conf spark.sql.catalog.unity_iceberg.type=rest \
   --conf spark.sql.catalog.unity_iceberg.uri=http://localhost:8080/api/2.1/unity-catalog/iceberg \
   --conf spark.sql.catalog.unity_iceberg.warehouse=unity_iceberg \
   --conf spark.sql.catalog.unity_iceberg.token=some_token \
   --conf spark.sql.defaultCatalog=unity_iceberg
```

## Create Database

Execute the following SQL command in Spark SQL.

```sql
CREATE DATABASE iceberg_db;
```

In another terminal:

```shell
./bin/uc schema get --full_name unity_iceberg.iceberg_db --output jsonPretty | jq 'del(..|nulls)'
```

```json
{
  "name": "iceberg_db",
  "catalog_name": "unity_iceberg",
  "properties": {
    "owner": "jacek"
  },
  "full_name": "unity_iceberg.iceberg_db",
  "created_at": 1794163853404,
  "updated_at": 1794163853404,
  "schema_id": "76ec0094-6adf-40ee-a939-9deda2e985a1"
}
```

## Create Table

In Spark SQL, execute the following `CREATE TABLE` command.

```sql
CREATE TABLE iceberg_db.people (id bigint, name string)
USING iceberg;
```

In another terminal, list the files under the `storage_location`.

```shell
tree /tmp/uc-storage-root/
```

```text
/tmp/uc-storage-root/
└── __unitystorage
    └── catalogs
        └── c1bf40a0-6348-4cee-a3b0-c59229a288b3
            └── tables
                └── f8580c84-72c0-4f8e-a39f-c09868ee8f5f
                    └── metadata
                        └── 00000-e9d808db-bfcb-462d-9e48-34aa41dd4028.metadata.json

7 directories, 1 file
```

## Write Data

```sql
INSERT INTO iceberg_db.people
VALUES (0, 'Jacek'), (1, 'Agata'), (2, 'Maksym');
```

## Read Data

```sql
SELECT * FROM iceberg_db.people;
```

```text
0       Jacek
1       Agata
2       Maksym
```

## Row-Level Merge Updates

```sql
MERGE INTO iceberg_db.people p
USING (SELECT * FROM VALUES (0, 'JACEK'), (3, 'Patryk'), (4, 'Iweta') AS u(id,name)) u
ON p.id = u.id
WHEN MATCHED THEN UPDATE SET p.name = u.name
WHEN NOT MATCHED THEN INSERT *;
```

```sql
SELECT * FROM iceberg_db.people ORDER BY 1;
```

```text
0       JACEK
1       Agata
2       Maksym
3       Patryk
4       Iweta
```
