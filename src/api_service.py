from typing import List, Generator
import logging

import requests


logger = logging.getLogger('airflow.task')

HACKER_NEWS_URL = 'https://hacker-news.firebaseio.com/v0/'


def get_beststories() -> List[int]:
    """
    Get high score stories ids
    """
    response = requests.get(HACKER_NEWS_URL + 'beststories.json')
    result = response.json()
    return result


def fetch_story_data(story_ids: List[int]) -> Generator[dict, None, None]:
    """
    Yield detailed stories information from API
    """
    for story_id in story_ids:
        url = HACKER_NEWS_URL + f'item/{story_id}.json'
        response = requests.get(url)
        yield response.json()
