---
hide:
- navigation
---

# Demo: Spark Connector and External Tables on AWS S3

!!! warning "Work in Progress"
    This page is a work in progress until this warning disappears.

``` bash
./bin/spark-sql \
  --name "uc-external-tables-s3" \
  --packages "org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_{{ scala.version }}:{{ delta.version }},io.unitycatalog:unitycatalog-spark_{{ scala.version }}:0.2.0-SNAPSHOT" \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog" \
  --conf "spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
  --conf "spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog" \
  --conf "spark.sql.catalog.unity.uri=http://localhost:8080" \
  --conf "spark.sql.catalog.unity.token=$(cat ../unitycatalog/etc/conf/token.txt)" \
  --conf "spark.sql.defaultCatalog=unity"
```
