# UnityAccessEvaluator

## Evaluate Authorization Expression { #evaluate }

``` java
boolean evaluate(
  UUID principal,
  String expression,
  Map<SecurableType, Object> resourceIds)
```

`evaluate` returns whatever the given `expression` has been evaluated to for the given `principal` and the resource IDs.

---

`evaluate` creates a `StandardEvaluationContext` (Spring Expression Language) with `Privileges` root object.

`evaluate` registers the following functions in the `StandardEvaluationContext`:

Function | Handler
-|-
authorize | [authorizeHandle](UnityCatalogAuthorizer.md#authorize)
authorizeAny | [authorizeAnyHandle](UnityCatalogAuthorizer.md#authorizeAny)
authorizeAll | [authorizeAllHandle](UnityCatalogAuthorizer.md#authorizeAll)

`evaluate` sets the following variables in the `StandardEvaluationContext`:

Variable | Value
-|-
 deny | FALSE
 permit | TRUE
 defer | TRUE
 principal | The given `principal`

`evaluate` sets variables (in the `StandardEvaluationContext`) for every resource ID (in the given `resourceIds`).

`evaluate` requests this [ExpressionParser](#parser) to evaluate the expression (in the `StandardEvaluationContext`).

`evaluate` prints out the following DEBUG message to the logs:

``` text
evaluating [expression] = [result]
```

---

`evaluate` is used when:

* `UnityAccessDecorator` is requested to [check authorization](UnityAccessDecorator.md#checkAuthorization)
* `UnityAccessEvaluator` is requested to [filter](#filter)
* `TemporaryModelVersionCredentialsService` is requested to [authorizeForOperation](../server/TemporaryModelVersionCredentialsService.md#authorizeForOperation)
* `TemporaryTableCredentialsService` is requested to [authorizeForOperation](../server/TemporaryTableCredentialsService.md#authorizeForOperation)
* `TemporaryVolumeCredentialsService` is requested to [authorizeForOperation](../server/TemporaryVolumeCredentialsService.md#authorizeForOperation)

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.auth.decorator.UnityAccessEvaluator` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

``` text
logger.UnityAccessEvaluator.name = io.unitycatalog.server.auth.decorator.UnityAccessEvaluator
logger.UnityAccessEvaluator.level = all
```

Refer to [Logging](../logging.md).
