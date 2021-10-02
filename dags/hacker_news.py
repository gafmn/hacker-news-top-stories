from typing import List
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
    def fetch_data() -> List[int]:
        result = get_beststories()
        return result[:150]

    @task()
    def parse_data():
        print('Lol')

    @task()
    def save_data():
        print('meow')


    task1 = fetch_data()
    task2 = parse_data()
    task3 = save_data()

    task1 >> task2 >> task3     # type: ignore


dag = hacker_news()
