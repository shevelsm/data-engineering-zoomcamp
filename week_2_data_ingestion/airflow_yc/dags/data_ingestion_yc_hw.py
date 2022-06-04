import os
import logging

from datetime import datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import boto3
import pyarrow.csv as pv
import pyarrow.parquet as pq
from requests import session


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BUCKET = os.environ.get("YCS_BUCKET")


def format_to_parquet(src_file, dest_file):
    if not src_file.endswith(".csv"):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, dest_file)


def upload_to_ycs(local_file, bucket, object_name):
    session = boto3.session.Session()
    s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")
    s3.upload_file(local_file, bucket, object_name)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}


def download_upload_dag(
    dag,
    dataset_url,
    local_parquet_path_template,
    ycs_path_template,
):
    with dag:
        download_dataset_task = BashOperator(
            task_id="download_dataset_task",
            bash_command=f"curl -sSLf {dataset_url} > {local_parquet_path_template}",
        )


        local_to_ycs_task = PythonOperator(
            task_id="local_to_ycs_task",
            python_callable=upload_to_ycs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": ycs_path_template,
                "local_file": local_parquet_path_template,
            },
        )

        rm_task = BashOperator(
            task_id="rm_task",
            bash_command=f"rm {local_parquet_path_template}",
        )

        download_dataset_task >> local_to_ycs_task >> rm_task


def download_parquetize_upload_dag(
    dag,
    dataset_url,
    local_csv_path_template,
    local_parquet_path_template,
    ycs_path_template,
):
    with dag:
        download_dataset_task = BashOperator(
            task_id="download_dataset_task",
            bash_command=f"curl -sSLf {dataset_url} > {local_csv_path_template}",
        )

        format_to_parquet_task = PythonOperator(
            task_id="format_to_parquet_task",
            python_callable=format_to_parquet,
            op_kwargs={
                "src_file": local_csv_path_template,
                "dest_file": local_parquet_path_template,
            },
        )

        local_to_ycs_task = PythonOperator(
            task_id="local_to_ycs_task",
            python_callable=upload_to_ycs,
            op_kwargs={
                "bucket": BUCKET,
                "object_name": ycs_path_template,
                "local_file": local_parquet_path_template,
            },
        )

        rm_task = BashOperator(
            task_id="rm_task",
            bash_command=f"rm {local_csv_path_template} {local_parquet_path_template}",
        )

        download_dataset_task >> format_to_parquet_task >> local_to_ycs_task >> rm_task


# https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.parquet
URL_PREFIX = "https://s3.amazonaws.com/nyc-tlc/trip+data"

YELLOW_TAXI_URL_TEMPLATE = (
    URL_PREFIX + "/yellow_tripdata_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
YELLOW_TAXI_PARQUET_FILE_TEMPLATE = (
    AIRFLOW_HOME + "/yellow_tripdata_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
YELLOW_TAXI_YCS_PATH_TEMPLATE = "raw/yellow_tripdata/year={{ execution_date.strftime('%Y') }}/{{ execution_date.strftime('%m') }}.parquet"

yellow_taxi_data_dag = DAG(
    dag_id="yellow_taxi_data",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019, 1, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=["de-zoomcamp"],
)

download_upload_dag(
    dag=yellow_taxi_data_dag,
    dataset_url=YELLOW_TAXI_URL_TEMPLATE,
    local_parquet_path_template=YELLOW_TAXI_PARQUET_FILE_TEMPLATE,
    ycs_path_template=YELLOW_TAXI_YCS_PATH_TEMPLATE,
)


# https://nyc-tlc.s3.amazonaws.com/trip+data/fhv_tripdata_2021-01.parquet
URL_PREFIX = "https://s3.amazonaws.com/nyc-tlc/trip+data"

FHV_TAXI_URL_TEMPLATE = (
    URL_PREFIX + "/fhv_tripdata_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
FHV_TAXI_PARQUET_FILE_TEMPLATE = (
    AIRFLOW_HOME + "/fhv_tripdata_{{ execution_date.strftime('%Y-%m') }}.parquet"
)
FHV_TAXI_YCS_PATH_TEMPLATE = "raw/fhv_tripdata/year={{ execution_date.strftime('%Y') }}/{{ execution_date.strftime('%m') }}.parquet"

fhv_taxi_data_dag = DAG(
    dag_id="fhv_taxi_data",
    schedule_interval="0 7 2 * *",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2020, 1, 1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=["de-zoomcamp"],
)

download_upload_dag(
    dag=fhv_taxi_data_dag,
    dataset_url=FHV_TAXI_URL_TEMPLATE,
    local_parquet_path_template=FHV_TAXI_PARQUET_FILE_TEMPLATE,
    ycs_path_template=FHV_TAXI_YCS_PATH_TEMPLATE,
)


# https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

ZONES_URL_TEMPLATE = "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
ZONES_CSV_FILE_TEMPLATE = AIRFLOW_HOME + "/taxi_zone_lookup.csv"
ZONES_PARQUET_FILE_TEMPLATE = AIRFLOW_HOME + "/taxi_zone_lookup.parquet"
ZONES_YCS_PATH_TEMPLATE = "raw/taxi_zone/taxi_zone_lookup.parquet"

zones_data_dag = DAG(
    dag_id="zones_data",
    schedule_interval="@once",
    start_date=days_ago(1),
    default_args=default_args,
    catchup=True,
    max_active_runs=3,
    tags=["de-zoomcamp"],
)

download_parquetize_upload_dag(
    dag=zones_data_dag,
    dataset_url=ZONES_URL_TEMPLATE,
    local_csv_path_template=ZONES_CSV_FILE_TEMPLATE,
    local_parquet_path_template=ZONES_PARQUET_FILE_TEMPLATE,
    ycs_path_template=ZONES_YCS_PATH_TEMPLATE,
)
