#!/bin/sh

# Waiting metastore-db to start
sleep 5

set +e
if schematool -dbType mysql -info -verbose; then
    echo "Hive metastore schema verified."
else
    if schematool -dbType mysql -initSchema -verbose; then
        echo "Hive metastore schema created."
    else
        echo "Error creating hive metastore: $?"
    fi
fi
set -e

start-metastore