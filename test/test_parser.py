import re

import pytest
import requests

from swgoh_forum_parser.parser.swgoh_forum_parser import SwgohForumParser
from swgoh_forum_parser.parser.constants import DOMAIN, GAME_NEWS_URI


class TestParser:

    @pytest.fixture()
    def mock_sleep_time(self, mocker):
        mocker.patch('time.sleep')

    @pytest.fixture()
    def mock_requests(self, requests_mock):
        page_not_found_matcher = re.compile(f'{DOMAIN}{GAME_NEWS_URI}/p\\d+/')
        with open('test/sample_html_pages/not_found_page.html') as f:
            requests_mock.get(page_not_found_matcher, text=f.read())

        first_page_url = f'{DOMAIN}{GAME_NEWS_URI}/p1/'
        with open('test/sample_html_pages/main_page.html') as f:
            requests_mock.get(first_page_url, text=f.read())

    @pytest.fixture()
    def parser(self):
        parser = SwgohForumParser()
        parser.set_url(DOMAIN+GAME_NEWS_URI)

        return parser

    def test_links_count(self, parser, mock_requests, mock_sleep_time):

        links = parser.get_posts_urls(100)

        assert len(links) == 10
