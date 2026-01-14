import time
from typing import Any
from prodexa.cache.base import CacheBackend


class MemoryCache(CacheBackend):
    def __init__(self):
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if not entry:
            return None

        expires_at, value = entry
        if expires_at < time.time():
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: int) -> None:
        expires_at = time.time() + ttl
        self._store[key] = (expires_at, value)
