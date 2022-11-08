from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import asdict

from custom_dataclasses import Post, Posts
from request_decorators import delay_request, retry

import requests
import json
import logging


logging.basicConfig()
handle = "my-app"
logger = logging.getLogger(handle)
logger.setLevel(logging.DEBUG)

DEV_NEWS_URL = 'https://forums.galaxy-of-heroes.starwars.ea.com/categories/news-and-announcements-'
GAME_NEWS_URL = 'https://forums.galaxy-of-heroes.starwars.ea.com/categories/game-updates'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}


class SwgohForumParser:
    url: str
    page: int

    def set_url(self, url: str) -> None:
        self.url = url
        self.page = 1

    def _get_posts_urls(self, num_links: int) -> list[str]:
        links = list()

        while len(links) < num_links:
            logger.info(f'Get post links from {self.page} page')

            page_links = self._get_posts_urls_from_page()
            links.extend(page_links)
            self.page += 1

        return links[:num_links]

    @retry(3)
    @delay_request(3)
    def _get_posts_urls_from_page(self) -> list[str]:
        response = requests.get(url=self.url + f'/p{self.page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        post_links_tags = soup.find(class_='DataTable DiscussionsTable').find_all('a', class_='Title')
        post_links = [tag['href'] for tag in post_links_tags]

        return post_links

    @retry(3)
    @delay_request(3)
    def _parse_post(self, url: str) -> Post:
        url_slug = url.split('/')[-1]
        logger.info(f'Get content from page {url_slug}')

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        author = soup.find('a', class_='Username js-userCard').text

        created_date_string = soup.find('a', class_='Permalink').text
        created_at = datetime.strptime(created_date_string, '%B %d, %Y %I:%M%p').strftime('%Y-%m-%d %H:%M:%S')

        title = soup.find('div', {'id': 'Item_0'}).find('h1').text

        content = soup.find(class_='Message').text

        post = Post(url=url,
                    author=author,
                    created_at=created_at,
                    title=title,
                    content=content)

        return post

    def parse(self, num_links: int):
        links = self._get_posts_urls(num_links)

        parsed_posts = Posts([self._parse_post(link) for link in links])
        return parsed_posts


logger.info('start')
parser = SwgohForumParser()
parser.set_url(GAME_NEWS_URL)
posts = parser.parse(15)

with open('../results.json', 'w') as f:
    f.write(json.dumps(asdict(posts), indent=4, ensure_ascii=False))
