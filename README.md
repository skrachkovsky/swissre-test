Install
=======

```sh
docker build --tag swissre-test .
docker run --name swissre-test -v /path-for-your-volume-for-input-output-data:/exchange-dir:rw -tid swissre-test
```

You have to mount one volume at least to provide access to input/output data outside the container.

Run
===

Enter the container

```sh
docker exec -it swissre-test sh
```

Run tests (optional)

```sh
pytest
```

Run the command for getting help

```sh
python -m swissre_test --help
```

Operation example

```sh
python -m swissre_test squid /exchange-dir/access.log eps /exchange-dir/eps-res.json json
````