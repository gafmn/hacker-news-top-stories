from functools import total_ordering
from typing import Generator, List
import logging
import sys

from airflow.decorators import dag, task    # type: ignore
from airflow.utils.dates import days_ago    # type: ignore

from src.api_service import (
        get_beststories,
        fetch_story_data
)

DEFAULT_ARGS = {'owner': 'airflow'}
logging.info(sys.path)

@dag(
    dag_id='hacker_news',
    default_args=DEFAULT_ARGS,
    schedule_interval=None, 
    start_date=days_ago(2)
)
def hacker_news():
    @task()
    def fetch_story_ids() -> List[int]:
        story_ids = get_beststories()
        return story_ids

    @task()
    def fetch_stories_data(**context) -> List[dict]:
        to_save = list()
        ti = context['ti']
        data = ti.xcom_pull(task_ids='fetch_story_ids')

        stories_generator = fetch_story_data(data)

        for item in stories_generator:
            to_save.append(item)

        return to_save

    @task()
    def save_data():
        pass


    task1 = fetch_story_ids()
    task2 = fetch_stories_data()
    task3 = save_data()

    task1 >> task2 >> task3     # type: ignore


dag = hacker_news()
