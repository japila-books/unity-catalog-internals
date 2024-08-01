# Docker Support

As of [this commit]({{ uc.commit }}/7564c7771ed655feb11ba3d5789fd3b7065a99ee), Unity Catalog's Localhost Server and CLI can be launched in a Docker container.

## Build Docker Image

```console
./docker/bin/build-uc-server-docker
```

```console
./docker/bin/build-uc-cli-docker
```

## Run Unity Catalog in Docker

```console
$ docker image ls --filter=reference='unitycatalog:*'
REPOSITORY     TAG              IMAGE ID       CREATED         SIZE
unitycatalog   0.2.0-SNAPSHOT   c788d0d453b6   8 minutes ago   329MB
```

```console
./docker/bin/start-uc-server-in-docker
```
