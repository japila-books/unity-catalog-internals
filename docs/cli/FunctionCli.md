# FunctionCli

## Handling Command Line { #handle }

```java
void handle(
  CommandLine cmd,
  ApiClient apiClient)
```

`handle` handles the given `cmd`.

Subcommand | Params | Handler
-|-|-
 `call` | `full_name` | [executeFunction](#executeFunction)
 `get` | `full_name` | [getFunction](#getFunction)
 ... | | &nbsp;

---

`handle` is used when:

* `UnityCatalogCli` is [launched on command line](UnityCatalogCli.md#main) with `function` command

## Executing Function { #executeFunction }

```java
String executeFunction(
  FunctionsApi functionsApi,
  JSONObject json)
```

`executeFunction` requests the given `FunctionsApi` for the [function](../server/FunctionService.md#getFunction) (by the `full_name` parameter) and [executes it](PythonInvoker.md#invokePython) using `etc/data/function/python_engine.py` Python runtime.

!!! note
    `FunctionsApi` sends HTTP requests to [FunctionService](../server/FunctionService.md).

## Looking Up Function { #getFunction }

```java
String getFunction(
  FunctionsApi functionsApi,
  JSONObject json)
```

`getFunction` requests the given `FunctionsApi` for the [function](../server/FunctionService.md#getFunction) (by the `full_name` parameter) and converts it to JSON (using the [ObjectWriter](#objectWriter)).

!!! note
    `FunctionsApi` sends HTTP requests to [FunctionService](../server/FunctionService.md).

```text
$ ./bin/uc function get --full_name unity.default.sum --output jsonPretty
{
  "name" : "sum",
  "catalog_name" : "unity",
  "schema_name" : "default",
  "input_params" : {
    "parameters" : [ {
      "name" : "x",
      "type_text" : "int",
      "type_json" : "{\"name\":\"x\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}}",
      "type_name" : "INT",
      "type_precision" : null,
      "type_scale" : null,
      "type_interval_type" : null,
      "position" : 0,
      "parameter_mode" : null,
      "parameter_type" : null,
      "parameter_default" : null,
      "comment" : null
    }, {
      "name" : "y",
      "type_text" : "int",
      "type_json" : "{\"name\":\"y\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}}",
      "type_name" : "INT",
      "type_precision" : null,
      "type_scale" : null,
      "type_interval_type" : null,
      "position" : 1,
      "parameter_mode" : null,
      "parameter_type" : null,
      "parameter_default" : null,
      "comment" : null
    }, {
      "name" : "z",
      "type_text" : "int",
      "type_json" : "{\"name\":\"z\",\"type\":\"integer\",\"nullable\":true,\"metadata\":{}}",
      "type_name" : "INT",
      "type_precision" : null,
      "type_scale" : null,
      "type_interval_type" : null,
      "position" : 2,
      "parameter_mode" : null,
      "parameter_type" : null,
      "parameter_default" : null,
      "comment" : null
    } ]
  },
  "data_type" : "INT",
  "full_data_type" : "INT",
  "return_params" : null,
  "routine_body" : "EXTERNAL",
  "routine_definition" : "t = x + y + z\\nreturn t",
  "routine_dependencies" : null,
  "parameter_style" : "S",
  "is_deterministic" : true,
  "sql_data_access" : "NO_SQL",
  "is_null_call" : false,
  "security_type" : "DEFINER",
  "specific_name" : "sum",
  "comment" : "Add two numbers",
  "properties" : null,
  "full_name" : "unity.default.sum",
  "created_at" : 1720082975600,
  "updated_at" : null,
  "function_id" : "6b587147-128f-4f05-8a4f-173a18831bdf",
  "external_language" : "python"
}
```
