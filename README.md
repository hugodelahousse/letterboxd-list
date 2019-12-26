# Letterboxd List Exporter

This project allows you to have hourly json exports of your letterboxd
userlists (e.g. watchlist) in json format.
The output format is as follows:

```json
[
  {
    "imdb_id": "ttXXXXXXXX",
    "poster_url": "<url>",
    "title": "Some Movie (2019)"
  },
  ...
]
```

## Setup

Here are the steps to follow to export your own lists automatically:

1. [Create a gist on GitHub](https://gist.new), and write down the gist id.

2. Create a users.json file in the gist, containing an object
  with this structure:
  ```json
  {
    "<username_1>": ["<list name>", "<list name>"],
    "<username_2>": [...]
    ...
  }
  ```

3. Create a [GitHub access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) with gist access scope

4. Fork this repository

5. Add two secrets in the repository settings: `GIST_ID` with the previously created gist id as a value
  and `ACCESS_TOKEN` containing your GitHub access token

Every hour, the action will be triggered, and your gist will be updated if
necessary with your watchlist changes.

Most of the letterboxd requests are cached, so only a few requests are made every time the list
is refreshed.
