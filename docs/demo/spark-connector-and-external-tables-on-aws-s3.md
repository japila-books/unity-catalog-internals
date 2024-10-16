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
  --packages "org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_{{ scala.version }}:{{ delta.version }},io.unitycatalog:unitycatalog-spark_{{ scala.version }}:{{ uc.version }}" \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=io.unitycatalog.spark.UCSingleCatalog" \
  --conf "spark.hadoop.fs.s3.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
  --conf "spark.sql.catalog.unity=io.unitycatalog.spark.UCSingleCatalog" \
  --conf "spark.sql.catalog.unity.uri=http://localhost:8080" \
  --conf "spark.sql.catalog.unity.token=$(cat ../unitycatalog/etc/conf/token.txt)" \
  --conf "spark.sql.defaultCatalog=unity"
```

``` text
## Demo: Spark Connector and External Tables on AWS S3
s3.bucketPath.0=s3://japila-unitycatalog
s3.region.0=FIXME_region
s3.awsRoleArn.0=FIXME_awsRoleArn
s3.accessKey.0=FIXME_accessKey
s3.secretKey.0=FIXME_secretKey
```
