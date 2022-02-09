#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import logging

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    schema_name = params.schema
    url = params.url
    csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, schema=schema_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append')


    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

<<<<<<< HEAD
        df.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='append')
=======
            df.to_sql(name=table_name, con=engine, if_exists='append')
>>>>>>> upstream/main

            t_end = time()

<<<<<<< HEAD
        logging.info('inserted another chunk, took %.3f second' % (t_end - t_start))
=======
            print('inserted another chunk, took %.3f second' % (t_end - t_start))
>>>>>>> upstream/main

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--schema', required=True, help='schema name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)