import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Protocol, Optional, Dict


class Cache(Protocol):
    def get(self, key) -> Optional[Any]:
        pass

    def set(self, key, value):
        pass


class MemoryCache:
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def get(self, key) -> Optional[Any]:
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

    def load(self, cache: Dict[str, Any]):
        self._cache.update(cache)

    def dump(self) -> Dict[str, Any]:
        return self._cache


@contextmanager
def saved_memory_cache(path):
    cache = MemoryCache()
    if Path(path).exists():
        cache.load(json.load(open(path)))

    try:
        yield cache
    finally:
        json.dump(cache.dump(), open(path, "w"))
