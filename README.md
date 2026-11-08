# The Internals of Unity Catalog Online Book

[![Deploying the docs](https://github.com/japila-books/unity-catalog-internals/actions/workflows/ci.yml/badge.svg)](https://github.com/japila-books/unity-catalog-internals/actions/workflows/ci.yml)

The project contains the sources of [The Internals of Unity Catalog](https://books.japila.pl/unity-catalog-internals) online book.

## Local Preview

Use [just](https://just.systems/) to start [Zensical](https://zensical.org/)'s live-reload server (requires [uv](https://docs.astral.sh/uv/)):

```shell
just serve
```

Extra arguments are passed through to `zensical serve` (e.g., `just serve --open`).

Run `just` alone to list all available recipes.
