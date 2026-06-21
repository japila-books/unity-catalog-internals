# Repositories

## Creating Instance

`Repositories` takes the following to be created:

* <span id="sessionFactory"> `SessionFactory` ([Hibernate]({{ hibernate.api }}/org/hibernate/SessionFactory.html))
* <span id="serverProperties"> [ServerProperties](ServerProperties.md)

`Repositories` is created when:

* `UnityCatalogServer`  is requested to [initializeServer](UnityCatalogServer.md#initializeServer)
