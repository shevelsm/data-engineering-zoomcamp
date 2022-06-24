# My example of a DWH with Trino on Hive metastore
## Creating services with Docker Compose

Using docker-compose you set up Presto, Hadoop, and Minio containers for Presto to query data from Minio. Presto uses the Hadoop container for the metastore.

## Run Trino CLI untility
Now we can run Trino via docker exec
``` bash
docker exec -it trino-dwh trino