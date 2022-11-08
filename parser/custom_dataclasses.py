from dataclasses import dataclass


@dataclass
class Post:
    url: str
    author: str
    created_at: str
    title: str
    content: str


@dataclass
class Posts:
    posts: list[Post]