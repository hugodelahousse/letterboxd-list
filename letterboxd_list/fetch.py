from typing import Set

from letterboxd_list import letterboxd_parse
from requests_html import HTMLSession, HTMLResponse

URL_PATTERN = "https://letterboxd.com/{username}/{list_name}/"


def get_list_page(session: HTMLSession, page_url: str) -> HTMLResponse:
    return session.get(page_url)


def get_first_page_url(username: str, list_name: str) -> str:
    return URL_PATTERN.format(username=username, list_name=list_name)


def get_all_movie_slugs(
    session: HTMLSession, username: str, list_name: str
) -> Set[str]:
    movie_ids = set()
    page_url = get_first_page_url(username, list_name)

    while page_url:
        content = get_list_page(session, page_url)
        page_url = letterboxd_parse.get_next_page(content)
        movie_ids |= set(letterboxd_parse.get_movie_paths(content))

    return movie_ids


def get_movie_page(session: HTMLSession, movie_url: str):
    return session.get(movie_url)
