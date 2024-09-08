# ModelRepository

## Logging

Enable `ALL` logging level for `io.unitycatalog.server.persist.ModelRepository` logger to see what happens inside.

Add the following line to `etc/conf/server.log4j2.properties`:

```text
logger.ModelRepository.name = io.unitycatalog.server.persist.ModelRepository
logger.ModelRepository.level = all
```

Refer to [Logging](../logging.md).
