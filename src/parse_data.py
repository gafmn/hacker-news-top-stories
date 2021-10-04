import json
from typing import Generator
from datetime import datetime


def build_stories_info(stories_generator: Generator[dict, None, None]) -> str:
    stories_info = dict()

    now = datetime.now()    
    stories_info['date'] = now

    stories_info['articles'] = list()

    for item in stories_generator:
        story = dict()
        story['rating'] = item['score']
        story['name'] = item['title']
        story['link'] = item.get('url', 'there is no link')
        stories_info['articles'].append(story)

    result =  json.dumps(stories_info, default=str)

    return result
