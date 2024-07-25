# DeltaKernelWriteUtils

## Write Out Sample Data to Delta Table { #writeSampleDataToDeltaTable }

```java
String writeSampleDataToDeltaTable(
  String tablePath,
  List<ColumnInfo> columns,
  AwsCredentials tempCredentialResponse)
```

`writeSampleDataToDeltaTable`...FIXME

---

`writeSampleDataToDeltaTable` is used when:

* `TableCli` is requested to [write to a table](TableCli.md#writeTable)
