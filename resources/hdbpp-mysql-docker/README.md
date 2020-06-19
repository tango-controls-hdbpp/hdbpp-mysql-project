# hdbpp-mysql-docker

Test Docker image for quickly setting up a test database to develop against. This has not been tested as a production database, but since its derived from the original MySQL Docker image there is no reason it should not be suitable for simple deployments

The container includes the following schema:

- hdb_innodb_schema.sql - The base tables etc.
- hdb_innodb_partition.sql - Partitioning based on time of tables

Any schema extensions currently have to added by hand.

## Building

Build the docker image using the Makefile:

```bash
make
```

If using a Docker registry then the Makefile can push the image to your registry (remember to update docker commands to include your registry address):

```bash
export DOCKER_REGISTRY=<your registry here>
make push
```

To clean an existing build:

```bash
make clean
```

## Running

The container can be run with persistent storage:

```bash
docker run --rm -d -p 3306:3306 -p 33060:33060 -v /your/mysql/data/dir:/var/lib/mysql -e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='password' --name hdbpp-test-innodb hdbpp-mysql-innodb:latest --innodb_buffer_pool_size=1G --innodb_flush_method=O_DIRECT
```

Or without persistent storage:

```bash
docker run --rm -d -p 3306:3306 -p 33060:33060 -e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='password' --name hdbpp-test-innodb hdbpp-mysql-innodb:latest --innodb_buffer_pool_size=1G --innodb_flush_method=O_DIRECT
```

## License

The source code is released under the LGPL3 license and a copy of this license is provided with the code.
