# Persistent Storage

Unity Catalog's [Localhost Reference Server](../server/index.md) uses [Hibernate](HibernateUtil.md) as the persistence layer to manage asset metadata.

Unity Catalog uses `etc/conf/hibernate.properties` configuration file to set up a JDBC-compatible database system. There are sample configuration files for MySQL and PostgreSQL.

By default, Localhost Reference Server uses [H2 Database Engine](https://www.h2database.com/) to store metadata (in `etc/db/h2db.mv.db` file).

With `server.env` property being `test`, Unity Catalog uses the following properties:

Hibernate Property | Value
-|-
 `hibernate.connection.driver_class` | `org.h2.Driver`
 `hibernate.connection.url` | `jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1`
 `hibernate.hbm2ddl.auto` | `create-drop`
