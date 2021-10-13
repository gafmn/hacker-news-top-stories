# Hacker News fetcher

Service saves every one hour top 10 best stories from Hacker News site.

For convenience [API of Hacker News](https://github.com/HackerNews/API) was used.

[![](https://img.shields.io/github/workflow/status/gafmn/hacker-news-top-stories/CheckTyping?logo=GitHub&style=for-the-badge)](https://github.com/gafmn/hacker-news-top-stories/actions/workflows/main.yml)

## Pre requirements

Docker and docker-compose

## Setup environment

Create file `.env` in root of project

Default setup for project
```
BUCKET_MINIO_PATH=articles/ycombinator/top/  # key for stories info in bucket
BUCKET_MINIO_FILENAME=top.json  # filename in bucket with stories info
BUCKET_MINIO_NAME=stage  # name of bucket
MINIO_DATA=/mnt/data  # mount of minio data
MINIO_USER=admin  # minio user
MINIO_PASSWORD=password  # minio user's password
MINIO_IS_SECURE=False  # is require ssl
MINIO_CONN_NAME=my_conn_S3 # airflow connection name

HACKER_NEWS_URL=https://hacker-news.firebaseio.com/v0/  # base url for fetching stories info

# Airflow setup
AIRFLOW_EXECUTOR=CeleryExecutor
AIRFLOW_SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
AIRFLOW_CELERY_RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
AIRFLOW_CELERY_BROKER_URL=redis://:@redis:6379/0
AIRFLOW_FERNET_KEY=
AIRFLOW_DAGS_ARE_PAUSED_AT_CREATION=True
AIRFLOW_LOAD_EXAMPLES=False

AIRFLOW_DAGS_PATH=./dags  # path to dags in local machine
AIRFLOW_LOGS_PATH=./logs  # path to logs in local machine
AIRFLOW_USER=airflow  # airflow user
AIRFLOW_PASSWORD=airflow  # airflow user's password

# Postgres setup
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

```

## Create connection in airflow
Fill **fields**

`Conn id`: `MINIO_CONN_NAME`

`Host`: minio

`Port`: 9000

`Extra`: 
```
{
  "aws_access_key_id": MINIO_USER, 
  "aws_secret_access_key": MINIO_PASSWORD, 
  "host": "http://minio:9000"
}
```

## How to run project

```
docker-compose up -d --build
```

Airflow running on 8080 port

Check on `localhost:8080`

 ## How to run test
 
 Make sure that `pytest` is installed in your environment
 
 ```
 pytest tests
 ```
