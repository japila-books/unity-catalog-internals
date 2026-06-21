# Localhost Reference Server

Unity Catalog comes with [Localhost Reference Server](UnityCatalogServer.md) that can be launched on command line using [bin/start-uc-server](#start-uc-server) utility.

## start-uc-server Shell Script { #start-uc-server }

`start-uc-server` runs [UnityCatalogServer](UnityCatalogServer.md) to [handle REST API requests](UnityCatalogServer.md#addServices) (at the port specified using [`--port` option](OptionParser.md#port)).

``` console
❯ ./bin/start-uc-server -h
usage: bin/start-uc-server
 -h,--help         Print help message.
 -p,--port <arg>   Port number to run the server on. Default is 8080.
 -v,--version      Display the version of the Unity Catalog server
```

!!! note
    The REST API requests can come from any Unity Catalog API-compatible client (e.g., [Unity Catalog CLI](../cli/index.md)).

## Server Configuration

The Localhost Reference Server uses `etc/conf/server.properties` file for [server configuration](ServerProperties.md#loadProperties).
