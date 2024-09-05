---
hide:
  - toc
---

# Logging

Unity Catalog uses [Log4j 2](https://logging.apache.org/log4j/2.x/) logging framework (through the [Simple Logging Facade for Java (SLF4J)](https://www.slf4j.org/) with [Apache Log4j SLF4J 2.0 Binding](https://logging.apache.org/log4j/2.x/log4j-slf4j-impl.html)).

There are two logging configuration files in `etc/conf`:

Component | Configuration File
-|-
[Unity Catalog CLI](cli/index.md) | `etc/conf/cli.log4j2.properties`
[Unity Catalog Server](server/index.md) | [etc/conf/server.log4j2.properties](#server.log4j2.properties)

## etc/conf/server.log4j2.properties { #server.log4j2.properties }

[Unity Catalog Server](server/index.md) uses `etc/conf/server.log4j2.properties` logging configuration file.

The following sample `server.log4j2.properties` sets up logging to standard output (_console_):

```text
status = warn

appender.console.name = stdout
appender.console.type = Console
appender.console.layout.type = PatternLayout
appender.console.layout.pattern = %d{YYYY-MM-dd HH:mm:ss} [%t] %-5p %c:%L - %m%n
appender.console.target = SYSTEM_OUT

rootLogger.level = info
rootLogger.appenderRefs = console
rootLogger.appenderRef.console.ref = stdout
```

## Automatic Configuration

[Automatic Configuration](https://logging.apache.org/log4j/2.x/manual/configuration.html)
