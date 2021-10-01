from typing import List, Generator

import requests


def get_beststories() -> List[int]:
    response = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json')
    result = response.json()
    return result


def fetch_story_data(story_ids) -> Generator[dict, None, None]:
    for story_id in story_ids:
        response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
        yield response.json()
