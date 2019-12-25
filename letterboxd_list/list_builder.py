import sys
from typing import List

from tqdm import tqdm

from requests_html import HTMLSession

from letterboxd_list.cache import Cache
from letterboxd_list.fetch import get_all_movie_slugs, get_movie_page
from letterboxd_list.letterboxd_parse import (
    get_imdb_url,
    get_imdb_id_from_url,
    get_movie_poster_url,
    get_movie_title,
)
import logging

from letterboxd_list.movie import Movie

LETTERBOXD_MOVIE_URL_PATTERN = "https://letterboxd.com{movie_slug}"

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_movie_list(
    imdb_id_cache: Cache, username: str, list_name: str = "watchlist"
) -> List[Movie]:
    session = HTMLSession()

    movie_slugs = get_all_movie_slugs(session, username, list_name)

    movie_list = []

    for slug in tqdm(movie_slugs):
        logger.info("Found movie slug: %s", slug)
        movie: Movie
        if movie := imdb_id_cache.get(slug):
            logger.info(
                "Movie found in cache: Title[%s] IMDb[%s]",
                movie["title"],
                movie["imdb_id"],
            )
            movie_list.append(movie)
            continue

        movie_page = get_movie_page(
            session, LETTERBOXD_MOVIE_URL_PATTERN.format(movie_slug=slug)
        )

        movie = {
            "title": get_movie_title(movie_page),
            "imdb_id": get_imdb_id_from_url(get_imdb_url(movie_page)),
            "poster_url": get_movie_poster_url(movie_page),
        }

        logger.info(
            "Found movie info: Title[%s] IMDb[%s]", movie["title"], movie["imdb_id"]
        )

        imdb_id_cache.set(slug, movie)
        movie_list.append(movie)

    return movie_list
