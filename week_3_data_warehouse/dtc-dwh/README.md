# My example of a DWH with Trino on Hive metastore
## Creating services with Docker Compose

Using docker-compose you set up Trino, Hive metastore and MariaDB containers for Trino to query data from S3 (yandexcloud). Presto uses the Hadoop container for the metastore.

Before running containers you need to insert your `S3_ACCESS_KEY` and `S3_SECRET_KEY` into:
- ./metastore/metastore-site.xml
- ./trino/catalog/hive.properties

After that you can start services with:
```bash
docker-compose up
```

## Run Trino CLI untility
Now we can run Trino via docker exec
``` bash
docker exec -it trino-dwh trino
```

To create tables in connected S3 bucket you can use `trino.sql `