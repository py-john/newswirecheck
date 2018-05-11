#!/usr/bin/env python3
import os
import json
import logging

from requests_html import HTML, HTMLSession
from mysms import textmyself

JSON_URL = 'http://www.rockstargames.com/newswire/get-posts.json?page=1'

PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_FILE = f'{PACKAGE_DIR}/newswire_check.log'
JSON_FILE = f'{PACKAGE_DIR}/newswire.json'

logging.basicConfig(filename=LOG_FILE,
                    format="%(asctime)s - %(message)s",
                    datefmt='%F %T')

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def get_last_title(j):
    """Get the last post title, the json contains html tags"""
    last_post = j['posts'][0]['title']
    last_title = HTML(html=last_post).text
    return last_title


def title_is_new(title):
    """Open and compare title to last saved title. Return boolean if updated"""
    try:
        with open(JSON_FILE, 'r') as f:
            stored = json.load(f)
    except FileNotFoundError:
        stored = {'Last Title': ''}
    if title != stored['Last Title']:
        stored['Last Title'] = title
        with open(JSON_FILE, 'w') as f:
            json.dump(stored, f, indent=4)
        return True
    return False


def main():
    """Run the scraper with the json response and text new title if updated """
    session = HTMLSession()
    json_res = session.get(JSON_URL).json()
    title = get_last_title(json_res)
    if title_is_new(title):
        textmyself(title)
        logger.info('Updated: ' + title)
    else:
        logger.info('Checked')


if __name__ == '__main__':
    main()
