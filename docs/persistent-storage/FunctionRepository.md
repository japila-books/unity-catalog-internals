# FunctionRepository

## SessionFactory { #SESSION_FACTORY }

`FunctionRepository` gets at [SessionFactory](HibernateUtil.md#getSessionFactory) in a static initializer.

??? note "Static Initializer"
    A **static initializer** declared in a class is executed when the class is initialized.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.7).

This `SessionFactory` is used for the following:

* [createFunction](#createFunction)
* [listFunctions](#listFunctions)
* [getFunction](#getFunction)
* [deleteFunction](#deleteFunction)

## Listing Functions { #listFunctions }

```java
ListFunctionsResponse listFunctions(
  String catalogName,
  String schemaName,
  Optional<Integer> maxResults,
  Optional<String> nextPageToken)
```

`listFunctions` requests this [SchemaRepository](#schemaRepository) for the [SchemaInfoDAO](SchemaRepository.md#getSchemaDAO) for the given catalog (`catalogName`) and schema (`schemaName`).

`listFunctions` creates the following Hibernate query (with the `schemaId` parameter being the ID of the schema):

```text
from FunctionInfoDAO f where f.schemaId = [schemaId]
```

In the end, `listFunctions` executes the query to list all the registered functions.

---

`listFunctions` is used when:

* `FunctionService` is requested to [list functions](../server/FunctionService.md#listFunctions)
