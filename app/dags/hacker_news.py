import logging
import logging.config
from typing import List
import os

from airflow.decorators import dag, task    # type: ignore
from airflow.utils.dates import days_ago    # type: ignore
from airflow.hooks.S3_hook import S3Hook    # type: ignore

from src.api_service import (   # type: ignore
    get_beststories,
    fetch_story_data
)
from src.parse_data import build_stories_info   # type: ignore
from src.db_connector import establish_connection   # type: ignore
from src.utils import hash_string   # type: ignore


logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

FILENAME = os.environ.get('BUCKET_MINIO_FILENAME', '')
BUCKET_PATH = os.environ.get('BUCKET_MINIO_PATH', '')
BUCKET_NAME = os.environ.get('BUCKET_MINIO_NAME', '')
IS_SECURE_CONN = os.environ.get('MINIO_IS_SECURE', '').lower() in ('true')
CONN_NAME = os.environ.get('MINIO_CONN_NAME')


DEFAULT_ARGS = {
    'owner': 'airflow',
    'provide_context': False,
}


@dag(
    dag_id='hacker_news',
    default_args=DEFAULT_ARGS,
    schedule_interval='@hourly',
    catchup=False,
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
    def save_stories_data_vault(**context):
        """
        """
        conn = establish_connection()
        logger.info(conn)
        logger.info(type(conn))

        execution_date = context['ts_nodash']

        logger.info('Load data from xCom')
        ti = context['ti']
        data = ti.xcom_pull(task_ids='fetch_story_ids')
        stories_generator = fetch_story_data(data)

        cursor = conn.cursor()

        for story in stories_generator:
            logger.info(f"Try to save {story['title']} with {story['id']}")

            name_hashed_key = hash_string(
                f"{story['title']}{execution_date}{str(story['id'])}"
            )
            link = story.get('url', 'there is no url')

            logger.info(f"With this hash {name_hashed_key}")
            logger.info(f"With this time stamp {execution_date}")

            query_h_articles = """
                INSERT INTO h_articles \
                (article_name, name_hashed_key, load_ts) \
                VALUES (%s, %s, %s)
            """
            query_satellite = """
                INSERT INTO hsat_article_descriptions \
                (hkey_article, score, url) \
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query_h_articles,
                (story['title'], name_hashed_key, execution_date)
            )
            cursor.execute(
                query_satellite,
                (name_hashed_key, story['score'], link)
            )
            conn.commit()

        cursor.close()
        conn.close()

    @task()
    def save_stories_s3(**context):
        """
        Save processed data to storage server
        """
        global FILENAME
        global BUCKET_PATH
        global BUCKET_NAME
        global IS_SECURE_CONN
        global CONN_NAME

        logger.info('Load data from xCom')
        ti = context['ti']
        stories_info = ti.xcom_pull(task_ids='process_stories_ids')

        execution_date = context['ts_nodash']

        client = S3Hook(aws_conn_id=CONN_NAME, verify=IS_SECURE_CONN)

        found = client.check_for_bucket(BUCKET_NAME)
        if found:
            logger.info(f'Bucket {BUCKET_NAME} alredy exist')
        else:
            logger.info(f'Bucket {BUCKET_NAME} not found')
            client.create_bucket(BUCKET_NAME)
            logger.info(f'Bucket {BUCKET_NAME} was created')

        logger.info('Try to load stories information to storage...')
        client.load_string(
            string_data=stories_info,
            key=f'{BUCKET_PATH}{execution_date}/{FILENAME}',
            replace=True,
            bucket_name=BUCKET_NAME
        )
        logger.info('Data was successfully loaded')

    task1 = fetch_story_ids()

    task2 = process_stories_ids()

    task3 = save_stories_s3()

    task4 = save_stories_data_vault()

    task1 >> task2 >> [task3, task4]   # type: ignore


dag = hacker_news()
