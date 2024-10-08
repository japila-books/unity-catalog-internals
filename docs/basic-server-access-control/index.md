# Basic Server Access Control

**Basic Server Access Control** adds access controls to the Unity Catalog server endpoints.

* Access control is optionally enabled through server configuration (`server.authorization=enable`)
* Resource endpoints all have access control rules that match access rules for Databricks Unity Catalog.
* An access control is defined by a principal, a resource and a privilege.
* Principals are currently only user entities.
* Access controls are hierarchically applied.
* A privilege assigned to a resource for a principal is active for all the children.
* A command-line interface is available to add, update, and delete authorizations.
* The root of the hierarchy is a catalog.
* There is a new concept of a metastore, which is primarily a resource to assign server-level privileges with.

??? note
    Basic Server Access Control is available since [this commit]({{ uc.commit }}/f9a9bf1f84cb4c7fa03ecb569ae19f306a7cd85b).

## Privileges

The initial set of privileges are as follows:

Privilege | Description
-|-
 `CREATE CATALOG` | Allows the principal to create catalogs
 `USE CATALOG` | Allows the principal to access/use a catalog
 `CREATE SCHEMA` | Allows the principal to create schemas within a catalog
 `USE SCHEMA` | Allows the principal to access/use the schema and child tables
 `CREATE_TABLE` | Allows the principal to create tables in the schema
 `SELECT` | Allows the principal to run queries against table(s)
 `CREATE_FUNCTION` | Allows principal to create functions in the schema
 `EXECUTE` | Allows the principal to execute function(s)
 `CREATE_VOLUME` | Allows principal to create volumes in the schema
 `READ VOLUME` | Allows the principal to access volumes within the catalog
 `CREATE MODEL` | Allows the principal to create models within a schema

## Unity Catalog CLI

The CLI interface provides a new `permission` command.

``` bash
./bin/uc permission create \
  --securable_type catalog \
  --name mycatalog \
  --principal user@myorg.com \
  --privilege "CREATE CATALOG`
```

``` bash
./bin/uc permission get \
  --securable_type catalog \
  --name unity
```

``` bash
./bin/uc permission delete \
  --securable_type table \
  --name mycatalog.myschema.table \
  --principal user@myorg.com \
  --privilege SELECT
```

## Framework

Basic Server Access Control is based on a framework that attempts to separate the concern of access control from the rest of the request handling and processing through annotation-based configuration, via `@AuthorizeExpression`, `@AuthorizeKey` and
`@AuthorizeKeys` added to each service entry point.

All requests are routed through the `UnityAccessDecorator` which decodes the request, parameters and authorization configuration to evaluate whether access should be allowed or denied.
