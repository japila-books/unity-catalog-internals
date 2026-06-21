# HibernateConfigurator

## Creating Instance

`HibernateConfigurator` takes the following to be created:

* [ServerProperties](#serverProperties)

`HibernateConfigurator` is created when:

* `UnityCatalogServer` is requested to [initializeServer](../server/UnityCatalogServer.md#initializeServer)

### ServerProperties { #serverProperties }

`HibernateConfigurator` is given a [ServerProperties](../server/ServerProperties.md) when [created](#creating-instance).

The `ServerProperties` is from [UnityCatalogServer.Builder](../server/UnityCatalogServer.Builder.md#serverProperties).
