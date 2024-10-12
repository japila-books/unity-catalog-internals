# UnityAccessDecorator

`UnityAccessDecorator` is used by [UnityCatalogServer](../server/UnityCatalogServer.md) to enforce access control rules on the following [API services](../server/UnityCatalogServer.md#addServices) endpoints:

* `/api/2.1/unity-catalog/`
* `/api/1.0/unity-control/` (except `/api/1.0/unity-control/auth/tokens`)

`UnityAccessDecorator` is used only when [UnityCatalogServer](../server/UnityCatalogServer.md) runs with [Server Authorization](index.md) enabled.

`UnityAccessDecorator` uses [AuthorizeExpression](AuthorizeExpression.md).

`UnityAccessDecorator` is a `DecoratingHttpServiceFunction` ([Armeria]({{ armeria.api }}/com/linecorp/armeria/server/DecoratingHttpServiceFunction.html)).

## Creating Instance

`UnityAccessDecorator` takes the following to be created:

* <span id="authorizer"> [UnityCatalogAuthorizer](UnityCatalogAuthorizer.md)

While being created, `UnityAccessDecorator` creates the [UnityAccessEvaluator](#evaluator) (with the [UnityCatalogAuthorizer](#authorizer)).

`UnityAccessDecorator` is created when:

* `UnityCatalogServer` is requested to [add the API services](../server/UnityCatalogServer.md#addServices) (with [Server Authorization](index.md) enabled)

### UnityAccessEvaluator { #evaluator }

`UnityAccessDecorator` creates an [UnityAccessEvaluator](UnityAccessEvaluator.md) (with the [UnityCatalogAuthorizer](#authorizer)) when [created](#creating-instance).

This `UnityAccessEvaluator` is used to [evaluate](UnityAccessEvaluator.md#evaluate) a principal to access securables while [checking authorization](#checkAuthorization).

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

When found, `serve` finds the [AuthorizeExpression](#findAuthorizeExpression) and the [AuthorizeKey](#findAuthorizeKeys) annotations (if defined on the method).

For the authorization expression and the authorization resource(s) found, `serve` [finds the principal](IdentityUtils.md#findPrincipalId) and [authorizeByRequest](#authorizeByRequest).

Otherwise, `serve` prints out the following WARN message to the logs:

``` text
Couldn't unwrap service.
```

### Find Service Method { #findServiceMethod }

```java
Method findServiceMethod(
  HttpService httpService)
```

??? note "Static Method"
    `findServiceMethod` is a Java **class method** to be invoked without a reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`findServiceMethod` tries to unwrap the given `HttpService` to be a `SimpleDecoratingHttpService` that is in turn tried to be unwrapped to an `AnnotatedService`.

If the given `HttpService` is unwrapped to an `AnnotatedService` successfully, `findServiceMethod` prints out the following DEBUG message to the logs:

``` text
serviceName = [serviceName], methodName = [methodName]
```

`findServiceMethod` gives the `Class` by the `serviceName` and then [finds the methods](#findMethodsByName) in the `Class` matching the `methodName`.

`findServiceMethod` returns the one and only `methodName` method of the `Class`, if found. Otherwise, it's undefined (`null`).

### Find Authorize Expression { #findAuthorizeExpression }

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

### Authorize By Request { #authorizeByRequest }

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

### Check Authorization { #checkAuthorization }

``` java
void checkAuthorization(
  UUID principal,
  String expression,
  Map<SecurableType, Object> resourceKeys)
```

`checkAuthorization`...FIXME

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.auth.decorator.UnityAccessDecorator` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.UnityAccessDecorator.name = io.unitycatalog.server.auth.decorator.UnityAccessDecorator
logger.UnityAccessDecorator.level = all
```

Refer to [Logging](../logging.md).
