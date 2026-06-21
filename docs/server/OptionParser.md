# OptionParser

`OptionParser` uses [Apache Commons CLI](https://commons.apache.org/proper/commons-cli/) library to parse the command-line options of [UnityCatalogServer](UnityCatalogServer.md).

```console
$ ./bin/start-uc-server --help
usage: bin/start-uc-server
 -h,--help         Print help message.
 -p,--port <arg>   Port number to run the server on. Default is 8080.
 -v,--version      Display the version of the Unity Catalog server
```

## -h, --help { #help }

Print help message.

## -p, --port { #port }

Port number to run the server on.

default: `8080`

## -v, --version { #version }

Display the version of the Unity Catalog server.
