# Localhost Reference Server

Unity Catalog comes with **Localhost Reference Server** that can be launched on command line using `./bin/start-uc-server` utility.

``` console
❯ ./bin/start-uc-server -h
usage: bin/start-uc-server
 -h,--help         Print help message.
 -p,--port <arg>   Port number to run the server on. Default is 8080.
 -v,--version      Display the version of the Unity Catalog server
```

`start-uc-server` runs [UnityCatalogServer](UnityCatalogServer.md) to [handle REST API requests](UnityCatalogServer.md#addServices) at a [port](UnityCatalogServer.md#port) (specified using `-p` or `--port` option or defaults to `8080`).
