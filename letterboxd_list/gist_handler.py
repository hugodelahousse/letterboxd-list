import argparse
import json
import logging
import sys
from typing import List, Any

from github import Github, InputFileContent
from github.Gist import Gist
from github.GistFile import GistFile

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.addHandler(logging.StreamHandler(sys.stdout))


def list_to_markdown(letterboxd_list: List[Any]):
    return "\n".join(
        f"[![{movie['title']}]({movie['poster_url']} \"{movie['title']}\")](https://www.imdb.com/title/{movie['imdb_id']}/)"
        for movie in letterboxd_list
    )


def update_gist(
    gist: Gist, username: str, watchlist: str, letterboxd_list: List[Any], posters=False
):
    filename = f"{username}-{watchlist}.json"
    posters_filename = f"{username}-{watchlist}-posters.md"

    letterboxd_list.sort(key=lambda e: e["title"])

    existing_file: GistFile
    if existing_file := gist.files.get(filename):
        try:
            existing_list = json.loads(existing_file.content)
            if letterboxd_list == existing_list:
                pass
                logger.info("No changes to list, skipping")
                return

        except ValueError:
            pass

    files = {filename: InputFileContent(json.dumps(letterboxd_list, indent=""))}

    if posters:
        files[posters_filename] = InputFileContent(list_to_markdown(letterboxd_list))

    gist.edit(files=files)


def main():
    from letterboxd_list.argparse_env_default import env_default

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--access-token", required=True, action=env_default("GITHUB_ACCESS_TOKEN")
    )

    parser.add_argument(
        "--gist-id", required=True, action=env_default("GITHUB_GIST_ID")
    )
    parser.add_argument(
        "--all-users", action="store_true",
    )

    args = parser.parse_args()

    from letterboxd_list.list_builder import get_movie_list

    github = Github(args.access_token)
    gist = github.get_gist(args.gist_id)

    if user_file := gist.files.get("users.json"):
        users = json.loads(user_file.content)
    else:
        raise RuntimeError("Could not find users.json file in gist `%s`", args.gist_id)

    from letterboxd_list.gist_cache import gist_cache

    full_list = {}
    with gist_cache(gist, "letterboxd-cache.json") as cache:
        for user, lists in users.items():
            for list_name in lists:
                movie_list = get_movie_list(cache, user, list_name)
                for movie in movie_list:
                    full_list[movie["imdb_id"]] = movie

                if args.all_users:
                    update_gist(
                        gist, user, list_name, movie_list,
                    )

    update_gist(
        gist, "all-users", "full-list", list(full_list.values()), posters=True,
    )


if __name__ == "__main__":
    main()
