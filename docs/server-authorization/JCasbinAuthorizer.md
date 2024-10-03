# JCasbinAuthorizer

`JCasbinAuthorizer` is a [UnityCatalogAuthorizer](UnityCatalogAuthorizer.md) based on [jCasbin]({{ jcasbin.github }}) open-source access control library.

`JCasbinAuthorizer` is used by [UnityCatalogServer](../server/UnityCatalogServer.md) with [server.authorization](index.md#server.authorization) enabled.

`JCasbinAuthorizer` uses `jcasbin_auth_model.conf` configuration file for access control models.

## Creating Instance

`JCasbinAuthorizer` takes no arguments to be created.

While being created, `JCasbinAuthorizer` reads the following configuration properties (using [HibernateUtils](../persistent-storage/HibernateUtils.md#getHibernateProperties)) to create a `JDBCAdapter` ([jdbc-adapter](https://github.com/jcasbin/jdbc-adapter)):

* `hibernate.connection.driver_class`
* `hibernate.connection.url`
* `hibernate.connection.user`
* `hibernate.connection.password`

`JCasbinAuthorizer` creates an access control model from `jcasbin_auth_model.conf`.

`JCasbinAuthorizer` creates the [Enforcer](#enforcer) that is configured to save policy rules automatically when they are added or removed.

`JCasbinAuthorizer` is created when:

* `UnityCatalogServer` is requested to [register the API services](../server/UnityCatalogServer.md#addServices)

## Enforcer { #enforcer }

`JCasbinAuthorizer` creates an `Enforcer` ([jCasbin]({{ jcasbin.api }}/org/casbin/jcasbin/main/Enforcer.html)) when [created](#creating-instance).

## Grant Authorization { #grantAuthorization }

??? note "UnityCatalogAuthorizer"

    ``` java
    boolean grantAuthorization(
      UUID principal,
      UUID resource,
      Privileges action)
    ```

    `grantAuthorization` is part of the [UnityCatalogAuthorizer](UnityCatalogAuthorizer.md#grantAuthorization) abstraction.

`grantAuthorization` requests the [Enforcer](#enforcer) to add an authorization rule (to the current `p` policy rule).
