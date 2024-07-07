# FunctionService

`FunctionService` is a [Unity Catalog API service](UnityCatalogServer.md) to handle HTTP requests at [/api/2.1/unity-catalog/functions](UnityCatalogServer.md#addServices) URL.

Method | URL | Handler | Params
-|-|-|-
 POST | | [createFunction](#createFunction) | &nbsp;
 DELETE | `/{name}` | [deleteFunction](#deleteFunction) | `name`<br>`force`
 GET | `/{name}` | [getFunction](#getFunction) | `name`
 GET | | [listFunctions](#listFunctions) | `catalog_name`<br>`schema_name`<br>`max_results`<br>`page_token` (not used)

## Listing Functions { #listFunctions }

```java
HttpResponse listFunctions(
  String catalogName,
  String schemaName,
  Optional<Integer> maxResults,
  Optional<String> pageToken)
```

`listFunctions` requests the [FunctionRepository](#FUNCTION_REPOSITORY) to [list functions](../persistent-storage/FunctionRepository.md#listFunctions).

```text
$ ./bin/uc function list --catalog unity --schema default
┌────────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│    NAME    │CATALOG_│SCHEMA_N│INPUT_PA│DATA_TYP│FULL_DAT│RETURN_P│ROUTINE_│ROUTINE_│ROUTINE_│PARAMETE│IS_DETER│SQL_DATA│IS_NULL_│SECURITY│SPECIFIC│COMMENT │PROPERTI│FULL_NAM│CREATED_│UPDATED_│FUNCTION│EXTERNAL│
│            │  NAME  │  AME   │  RAMS  │   E    │ A_TYPE │ ARAMS  │  BODY  │DEFINITI│DEPENDEN│R_STYLE │MINISTIC│_ACCESS │  CALL  │ _TYPE  │ _NAME  │        │   ES   │   E    │   AT   │   AT   │  _ID   │_LANGUAG│
│            │        │        │        │        │        │        │        │   ON   │  CIES  │        │        │        │        │        │        │        │        │        │        │        │        │   E    │
├────────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│sum         │unity   │default │{"par...│INT     │INT     │null    │EXTERNAL│t = x...│null    │S       │true    │NO_SQL  │false   │DEFINER │sum     │Add t...│null    │unity...│17200...│null    │6b587...│python  │
├────────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┼────────┤
│lowercase   │unity   │default │{"par...│STRING  │STRING  │null    │EXTERNAL│g = s...│null    │S       │true    │NO_SQL  │false   │DEFINER │lower...│Conve...│null    │unity...│17200...│null    │a1722...│python  │
└────────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
```

## Looking Up Function { #getFunction }

```java
HttpResponse getFunction(
  String name)
```

`listFunctions` requests the [FunctionRepository](#FUNCTION_REPOSITORY) for the [function](../persistent-storage/FunctionRepository.md#getFunction) by the given `name`.

```text
$ ./bin/uc function get --full_name unity.default.sum
┌────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        KEY         │                                               VALUE                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│NAME                │sum                                                                                                 │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CATALOG_NAME        │unity                                                                                               │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SCHEMA_NAME         │default                                                                                             │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│INPUT_PARAMS        │{"parameters":[{"name":"x","type_text":"int","type_json":"{\"name\":\"x\",\"type\":\"integer\",\"nul│
│                    │lable\":true,\"metadata\":{}}","type_name":"INT","type_precision":null,"type_scale":null,"type_inter│
│                    │val_type":null,"position":0,"parameter_mode":null,"parameter_type":null,"parameter_default":null,"co│
│                    │mment":null},{"name":"y","type_text":"int","type_json":"{\"name\":\"y\",\"type\":\"integer\",\"nulla│
│                    │ble\":true,\"metadata\":{}}","type_name":"INT","type_precision":null,"type_scale":null,"type_interva│
│                    │l_type":null,"position":1,"parameter_mode":null,"parameter_type":null,"parameter_default":null,"comm│
│                    │ent":null},{"name":"z","type_text":"int","type_json":"{\"name\":\"z\",\"type\":\"integer\",\"nullabl│
│                    │e\":true,\"metadata\":{}}","type_name":"INT","type_precision":null,"type_scale":null,"type_interval_│
│                    │type":null,"position":2,"parameter_mode":null,"parameter_type":null,"parameter_default":null,"commen│
│                    │t":null}]}                                                                                          │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│DATA_TYPE           │INT                                                                                                 │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│FULL_DATA_TYPE      │INT                                                                                                 │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│RETURN_PARAMS       │null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ROUTINE_BODY        │EXTERNAL                                                                                            │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ROUTINE_DEFINITION  │t = x + y + z\nreturn t                                                                             │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ROUTINE_DEPENDENCIES│null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PARAMETER_STYLE     │S                                                                                                   │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│IS_DETERMINISTIC    │true                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SQL_DATA_ACCESS     │NO_SQL                                                                                              │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│IS_NULL_CALL        │false                                                                                               │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SECURITY_TYPE       │DEFINER                                                                                             │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│SPECIFIC_NAME       │sum                                                                                                 │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│COMMENT             │Add two numbers                                                                                     │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│PROPERTIES          │null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│FULL_NAME           │unity.default.sum                                                                                   │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│CREATED_AT          │1720082975600                                                                                       │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│UPDATED_AT          │null                                                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│FUNCTION_ID         │6b587147-128f-4f05-8a4f-173a18831bdf                                                                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┤
│EXTERNAL_LANGUAGE   │python                                                                                              │
└────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
