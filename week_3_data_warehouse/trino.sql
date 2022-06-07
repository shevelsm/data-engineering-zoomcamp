-- Create schema for tables
CREATE SCHEMA IF NOT EXISTS hive.ny_taxi WITH (
    location = 's3a://dtc-data-lake-b1g6ec5r89keqf5e5kv5/raw'
);



-- Print list of possible table properties to set
SELECT
    *
FROM
    system.metadata.table_properties;



-- We need some properties:
-- external_location | varchar        | File system location URI for external table 
-- format            | varchar        | Hive storage format for the table. Possible values: [ORC, PARQUET, AVRO, RCBINARY, RCTEXT, SEQUENCEFILE, JSON, TEXTFILE, CSV]
-- partitioned_by    | array(varchar) | Partition columns   
-- Create table for yellow taxi data
CREATE TABLE IF NOT EXISTS hive.ny_taxi.yellow_tripdata (
    VendorID BIGINT,
    tpep_pickup_datetime BIGINT,
    tpep_dropoff_datetime BIGINT,
    passenger_count DOUBLE,
    trip_distance DOUBLE,
    RatecodeID DOUBLE,
    store_and_fwd_flag VARCHAR,
    PULocationID BIGINT,
    DOLocationID BIGINT,
    payment_type BIGINT,
    fare_amount DOUBLE,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE,
    congestion_surcharge DOUBLE,
    airport_fee DOUBLE,
    year VARCHAR
) WITH (
    external_location = 's3a://dtc-data-lake-b1g6ec5r89keqf5e5kv5/raw/yellow_tripdata',
    format = 'PARQUET',
    partitioned_by = ARRAY ['year']
);



-- Update info about partitions 
CALL system.sync_partition_metadata('hive.ny_taxi', 'yellow_tripdata', 'ADD');



-- Check total count of rows
SELECT
    COUNT(*)
FROM
    hive.ny_taxi.yellow_tripdata;



-- Check created partitions
SELECT
    *
FROM
    hive.ny_taxi."yellow_tripdata$partitions";



-- Create table for For-Hire Vehicle taxi data
CREATE TABLE IF NOT EXISTS hive.ny_taxi.fhv_tripdata (
    dispatching_base_num VARCHAR,
    pickup_datetime BIGINT,
    dropOff_datetime BIGINT,
    PUlocationID DOUBLE,
    DOlocationID DOUBLE,
    SR_Flag INTEGER,
    Affiliated_base_number VARCHAR,
    year VARCHAR
) WITH (
    external_location = 's3a://dtc-data-lake-b1g6ec5r89keqf5e5kv5/raw/fhv_tripdata',
    format = 'PARQUET',
    partitioned_by = ARRAY ['year']
);



-- Update info about partitions 
CALL system.sync_partition_metadata('hive.ny_taxi', 'fhv_tripdata', 'ADD');



-- Check total count of rows
SELECT
    COUNT(*)
FROM
    hive.ny_taxi.fhv_tripdata;



-- Check created partitions
SELECT
    *
FROM
    hive.ny_taxi."fhv_tripdata$partitions";