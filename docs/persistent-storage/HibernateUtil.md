# HibernateUtil

`HibernateUtil` is used to access the system-wide [SessionFactory](#sessionFactory) ([Hibernate]({{ hibernate.javadoc }}/org/hibernate/SessionFactory.html)).

## ServerPropertiesUtils { #properties }

`HibernateUtil` gets at the only instance of [ServerPropertiesUtils](../server/ServerPropertiesUtils.md#instance) in a static initializer.

??? note "Static Initializer"
    A **static initializer** declared in a class is executed when the class is initialized.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.7).

## SessionFactory { #sessionFactory }

`HibernateUtil` [creates a SessionFactory](#createSessionFactory) in a static initializer.

??? note "Static Initializer"
    A **static initializer** declared in a class is executed when the class is initialized.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.7).

This `SessionFactory` is used by the following:

* [CatalogRepository](CatalogRepository.md#sessionFactory)
* [FunctionRepository](FunctionRepository.md#SESSION_FACTORY)
* [SchemaRepository](SchemaRepository.md#sessionFactory)
* [TableRepository](TableRepository.md#sessionFactory)
* [VolumeRepository](VolumeRepository.md#sessionFactory)
* [IcebergRestCatalogService](../iceberg/IcebergRestCatalogService.md#sessionFactory)

## createSessionFactory { #createSessionFactory }

```java
SessionFactory createSessionFactory()
```

??? note "Static Method"
    `createSessionFactory` is a Java **class method** that is always invoked without reference to a particular object.

    Learn more in the [Java Language Specification]({{ java.spec }}/jls-8.html#jls-8.4.3.2).

`createSessionFactory`...FIXME
