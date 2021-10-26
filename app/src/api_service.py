from typing import List, Generator
import logging
import os

import requests


logger = logging.getLogger('airflow.task')

HACKER_NEWS_URL = os.environ.get('HACKER_NEWS_URL', '')


def get_beststories() -> List[int]:
    """
    Get high score stories ids
    """
    global HACKER_NEWS_URL

    response = requests.get(HACKER_NEWS_URL + 'beststories.json')
    result = response.json()
    return result


def fetch_story_data(story_ids: List[int]) -> Generator[dict, None, None]:
    """
    Yield detailed stories information from API
    """
    global HACKER_NEWS_URL

    for story_id in story_ids:
        url = HACKER_NEWS_URL + f'item/{story_id}.json'
        response = requests.get(url)
        yield response.json()
