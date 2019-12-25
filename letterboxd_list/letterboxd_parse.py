from pathlib import Path
from typing import Iterable, Optional

from requests_html import HTMLResponse


def get_next_page(response: HTMLResponse) -> Optional[str]:
    next_page = response.html.find(".next", first=True)
    if next_page:
        for page_url in next_page.absolute_links:
            return page_url

    return None


def get_movie_paths(response: HTMLResponse) -> Iterable[str]:
    posters = response.html.find(".film-poster")
    return map(lambda poster: poster.attrs["data-film-slug"], posters)


def get_imdb_url(movie_response: HTMLResponse) -> str:
    return movie_response.html.find('[data-track-action="IMDb"]', first=True).attrs[
        "href"
    ]


def get_imdb_id_from_url(url: str) -> str:
    path = Path(url)
    while path.parts and not str(path.stem).startswith("tt"):
        path = path.parent

    assert path.parts, "Could not parse IMDb URL"

    return str(path.stem)


def get_movie_poster_url(movie_response: HTMLResponse) -> str:
    return (
        movie_response.html.find(".film-poster", first=True)
        .find('img[itemprop="image"]', first=True)
        .attrs["src"]
    )


def get_movie_title(movie_response: HTMLResponse) -> str:
    return movie_response.html.find('meta[property="og:title"]', first=True).attrs[
        "content"
    ]
