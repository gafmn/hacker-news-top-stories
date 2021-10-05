from typing import List, Generator

import requests

HACKER_NEWS_URL = 'https://hacker-news.firebaseio.com/v0/'


def get_beststories() -> List[int]:
    response = requests.get(HACKER_NEWS_URL + 'beststories.json')
    result = response.json()
    return result


def fetch_story_data(story_ids: List[int]) -> Generator[dict, None, None]:
    for story_id in story_ids:
        response = requests.get(HACKER_NEWS_URL + f'item/{story_id}.json')
        yield response.json()
