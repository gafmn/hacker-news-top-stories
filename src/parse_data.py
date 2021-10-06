import json
import logging
from typing import Generator, Union, List, Dict, Any
from datetime import datetime

logger = logging.getLogger('parseStoriesInfo')

def build_stories_info(stories_generator: Generator[dict, None, None], execution_date: str) -> str:
    logger.info('Parse stories data')
    stories_info: Dict[str, Any] = dict()

    stories_info['execution_date'] = execution_date

    stories_info['articles'] = list()

    for item in stories_generator:
        logger.debug(f"Try to parse story {item['title']}")
        story = dict()
        story['rating'] = item['score']
        story['name'] = item['title']
        story['link'] = item.get('url', 'there is no link')
        stories_info['articles'].append(story)

    result =  json.dumps(stories_info, default=str)

    return result