import logging
import logging.config
from typing import List
from datetime import datetime

from airflow.decorators import dag, task    # type: ignore
from airflow.utils.dates import days_ago    # type: ignore

from src.api_service import (   # type: ignore
    get_beststories,
    fetch_story_data
) 
from src.parse_data import build_stories_info   # type: ignore

logger = logging.getLogger('hackerNews')

# Logger setup
logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler'
            }
        },
        'loggers': {
            'hackerNews': {
                'handlers': ['console']
            },
            'parseStoriesInfo': {
                'handlers': ['console']
            }
        }
    }
)

DEFAULT_ARGS = {
    'owner': 'airflow',
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
    def process_stories_ids(date: str, **context) -> str:
        """
        Get stories details and format it ro string
        """
        logger.info('Load data from xCom')
        ti = context['ti']
        data = ti.xcom_pull(task_ids='fetch_story_ids')

        execution_date = date

        logger.info('Generate stories data')
        stories_generator = fetch_story_data(data)
        stories_info = build_stories_info(stories_generator, execution_date)

        return stories_info

    @task()
    def save_data():
        """
        Save processed data to storage server
        """
        logger.info('Save stories data to minio')
        pass


    task1 = fetch_story_ids()

    execution_date = "{{ ts }}"
    task2 = process_stories_ids(execution_date)

    task3 = save_data()

    task1 >> task2 >> task3     # type: ignore


dag = hacker_news()
