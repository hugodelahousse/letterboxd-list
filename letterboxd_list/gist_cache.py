import json
from contextlib import contextmanager

from github import InputFileContent
from github.Gist import Gist

from letterboxd_list.cache import MemoryCache


@contextmanager
def gist_cache(gist: Gist, filename: str):
    cache = MemoryCache()
    original_cache = None
    if cache_file := gist.files.get(filename):
        content = cache_file.content
        original_cache = json.loads(content)
        cache.load(original_cache)

    try:
        yield cache
    finally:
        new_cache = cache.dump()
        if new_cache != original_cache:
            content = json.dumps(new_cache, indent="")
            gist.edit(files={filename: InputFileContent(content)})
