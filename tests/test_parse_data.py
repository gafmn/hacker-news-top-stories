from typing import Generator
from datetime import datetime
import json

from context import src
from src import parse_data  # type: ignore

def generate_stub_stories() -> Generator[dict, None, None]:
    """
    Stub stories data
    """
    for i in range(2):
        stub_data = {
                'title': 'Test' + str(i),
                'score': 1234,
                'url': 'some-url-here'
        }
        yield stub_data


def generate_stub_stories_without_url() -> Generator[dict, None, None]:
    """
    Stub stories data without providing url
    """
    for i in range(2):
        stub_data = {
                'title': 'Test' + str(i),
                'score': 1234,
                'url': 'there is no link'
        }
        yield stub_data


def test_build_stories_info():
    """
    Test module that extract necessary stories data and dumps it to string
    """
    
    execution_date = str(datetime.now())
    generator_stories = generate_stub_stories()

    res = parse_data.build_stories_info(generator_stories, execution_date)

    expected_res = {
            'execution_date': execution_date,
            'articles': [
                {
                    'rating': 1234,
                    'name': 'Test0',
                    'link': 'some-url-here'
                },
                {
                    'rating': 1234,
                    'name': 'Test1',
                    'link': 'some-url-here'
                }
            ]
    }

    expected_res = json.dumps(expected_res, default=str)

    assert expected_res == res


def test_build_stories_info_without_url():
    """
    Test module that extract necessary stories data without providing url
    """
    
    execution_date = str(datetime.now())
    generator_stories = generate_stub_stories_without_url()

    res = parse_data.build_stories_info(generator_stories, execution_date)

    expected_res = {
            'execution_date': execution_date,
            'articles': [
                {
                    'rating': 1234,
                    'name': 'Test0',
                    'link': 'there is no link'
                },
                {
                    'rating': 1234,
                    'name': 'Test1',
                    'link': 'there is no link'
                }
            ]
    }

    expected_res = json.dumps(expected_res, default=str)

    assert expected_res == res
