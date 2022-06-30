Install
=======

```sh
docker build --tag swissre-test .
```

Tests
=====

```sh
docker run --entrypoint pytest swissre-test
```

Help
====

```sh
docker run -i --rm swissre-test
```


Command example
===============

```sh
cat ~/access.log | docker run -i --rm swissre-test squid eps json > ~/result.json
```
