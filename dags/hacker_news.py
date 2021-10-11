import logging
import logging.config
from typing import List
import os

from airflow.decorators import dag, task    # type: ignore
from airflow.utils.dates import days_ago    # type: ignore

from src.api_service import (   # type: ignore
    get_beststories,
    fetch_story_data
) 
from src.parse_data import build_stories_info   # type: ignore


logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

FILENAME = os.environ.get('BUCKET_MINIO_FILENAME', '')
BUCKET_PATH = os.environ.get('BUCKET_MINIO_PATH', '')
BUCKET_NAME = os.environ.get('BUCKET_MINIO_NAME', '')

DEFAULT_ARGS = {
    'owner': 'airflow',
    'provide_context': False,
    'schedule_interval': '@hourly'
}

@dag(
    dag_id='hacker_news',
    default_args=DEFAULT_ARGS,
    start_date=days_ago(1)
)
def hacker_news():
    @task()
    def fetch_story_ids() -> List[int]:
        """
        Get stories ids for processing
        """
        logger.info('Get best stories from hacker news API')

        story_ids = get_beststories()
        
        return story_ids

    @task()
    def process_stories_ids(**context) -> str:
        """
        Get stories details and format it ro string
        """
        logger.info('Load data from xCom')
        ti = context['ti']
        data = ti.xcom_pull(task_ids='fetch_story_ids')

        execution_date = context['ts_nodash']
        logger.info(execution_date)

        logger.info('Generate stories data')
        stories_generator = fetch_story_data(data)
        stories_info = build_stories_info(stories_generator, execution_date)

        return stories_info

    @task()
    def save_data(**context):
        """
        Save processed data to storage server
        """
        import io

        from minio import Minio     # type: ignore

        global FILENAME
        global BUCKET_PATH
        global BUCKET_NAME

        logger.info('Save stories data to minio')

        logger.info('Load data from xCom')
        ti = context['ti']
        stories_info = ti.xcom_pull(task_ids='process_stories_ids')
        logger.info(os.environ.get('MINIO_SECURE'))

        client = Minio(
            endpoint='minio:9000',
            access_key=os.environ.get('MINIO_USER'),
            secret_key=os.environ.get('MINIO_PASSWORD'),
            secure=os.environ.get('MINIO_SECURE', 'False').lower() in ('true')
        )

        logger.info('Check if backet already exist...')
        if client.bucket_exists(BUCKET_NAME):
            logger.info('Backet alredy exist')
        else:
            client.make_bucket(BUCKET_NAME)

        logger.info('Prepare object to save to Minio')

        execution_date = context['ts_nodash']

        logger.info(execution_date)
        object_name = BUCKET_PATH + (execution_date) + '/' + FILENAME

        logger.info(object_name)

        logger.info('Convert stories info to stream of bytes')
        stories_info_bytes = bytes(stories_info, 'utf-8')
        logger.info(stories_info_bytes)
        stories_info_stream = io.BytesIO(stories_info_bytes)
        logger.info(stories_info_stream)


        logger.info(f'Put stories info to bucket with key {object_name}')
        client.put_object(
            bucket_name=BUCKET_NAME,
            data=stories_info_stream,
            object_name=object_name,
            length=len(stories_info_bytes),
        )


    task1 = fetch_story_ids()

    task2 = process_stories_ids()

    task3 = save_data()

    task1 >> task2 >> task3     # type: ignore


dag = hacker_news()
