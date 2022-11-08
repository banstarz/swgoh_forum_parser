import logging
import json
from dataclasses import asdict
from parser.swgoh_forum_parser import SwgohForumParser
from parser.constants import DOMAIN, GAME_NEWS_URI, DEV_NEWS_URI


logging.basicConfig()
handle = "my-app"
logger = logging.getLogger(handle)
logger.setLevel(logging.DEBUG)

logger.info('start')
parser = SwgohForumParser()
parser.set_url(DOMAIN+GAME_NEWS_URI)
posts = parser.parse(1)

with open('results.json', 'w') as f:
    f.write(json.dumps(asdict(posts), indent=4, ensure_ascii=False))
