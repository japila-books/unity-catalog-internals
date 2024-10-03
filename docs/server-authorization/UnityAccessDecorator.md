# UnityAccessDecorator

`UnityAccessDecorator` is used by [UnityCatalogServer](../server/UnityCatalogServer.md) to enforce access control rules on the [API services](../server/UnityCatalogServer.md#addServices):

* `/api/2.1/unity-catalog/`
* `/api/1.0/unity-control/` (except `/api/1.0/unity-control/auth/tokens`)

`UnityAccessDecorator` is used only when [UnityCatalogServer](../server/UnityCatalogServer.md) runs with [Server Authorization](index.md) enabled.

`UnityAccessDecorator` uses [AuthorizeExpression](AuthorizeExpression.md).

`UnityAccessDecorator` is a `DecoratingHttpServiceFunction` ([Armeria]({{ armeria.api }}/com/linecorp/armeria/server/DecoratingHttpServiceFunction.html)).

## Serve Incoming HTTP Request { #serve }

??? note "DecoratingHttpServiceFunction"

    ``` java
    HttpResponse serve(
      HttpService delegate,
      ServiceRequestContext ctx,
      HttpRequest req)
    ```

    `serve` is part of the `DecoratingHttpServiceFunction` ([Armeria]({{ armeria.api }}/com/linecorp/armeria/server/DecoratingHttpServiceFunction.html#serve(com.linecorp.armeria.server.HttpService,com.linecorp.armeria.server.ServiceRequestContext,com.linecorp.armeria.common.HttpRequest))) abstraction.

`serve` prints out the following DEBUG message to the logs:

``` text
AccessDecorator checking [path]
```

`serve` [finds the service method](#findServiceMethod).

When found, `serve`...FIXME

Otherwise, `serve` prints out the following WARN message to the logs:

``` text
Couldn't unwrap service.
```

### findAuthorizeExpression { #findAuthorizeExpression }

```java
String findAuthorizeExpression(
  Method method)
```

??? note "Static Method"
    `findAuthorizeExpression` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`findAuthorizeExpression` takes the [AuthorizeExpression](AuthorizeExpression.md) of the given `method`.

When found, `findAuthorizeExpression` prints out the following DEBUG message to the logs and returns the authorize expression value:

``` text
authorize expression = [annotation_value]
```

Otherwise, `findAuthorizeExpression` prints out the following DEBUG message to the logs and returns no authorize expression value (`null`):

``` text
authorize = (none found)
```

### authorizeByRequest { #authorizeByRequest }

``` java
HttpResponse authorizeByRequest(
  HttpService delegate,
  ServiceRequestContext ctx,
  HttpRequest req,
  UUID principal,
  List<KeyLocator> locators,
  String expression)
```

`authorizeByRequest`...FIXME

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.auth.decorator.UnityAccessDecorator` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.UnityAccessDecorator.name = io.unitycatalog.server.auth.decorator.UnityAccessDecorator
logger.UnityAccessDecorator.level = all
```

Refer to [Logging](../logging.md).
