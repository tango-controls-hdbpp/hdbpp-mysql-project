ARG MYSQL_VERSION
FROM mysql/mysql-server:${MYSQL_VERSION}

COPY build-files/schema/hdb_innodb_schema.sql  /docker-entrypoint-initdb.d/901_hdb_innodb_schema.sql
COPY build-files/schema/hdb_innodb_partition.sql  /docker-entrypoint-initdb.d/902_hdb_innodb_partition.sql
COPY build-files/schema/hdb_innodb_user.sql  /docker-entrypoint-initdb.d/903_hdb_innodb_user.sql

USER root
