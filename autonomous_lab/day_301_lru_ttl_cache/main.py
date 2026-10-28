"""
Thread-Safe In-Memory LRU Cache with TTL
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Tuple

class LRUTTLCache:
    """
    Least-Recently-Used (LRU) Cache supporting per-entry TTL (Time-To-Live).
    """
    def __init__(self, capacity: int, default_ttl_seconds: Optional[float] = None):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.default_ttl = default_ttl_seconds
        self._cache: OrderedDict[str, Tuple[Any, Optional[float]]] = OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            val, expiry = self._cache[key]
            if expiry is not None and time.monotonic() > expiry:
                del self._cache[key]
                self.misses += 1
                return None
            self._cache.move_to_end(key)
            self.hits += 1
            return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        with self._lock:
            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
            expiry = (time.monotonic() + ttl) if ttl is not None else None
            if key in self._cache:
                del self._cache[key]
            elif len(self._cache) >= self.capacity:
                self._cache.popitem(last=False)
            self._cache[key] = (value, expiry)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def size(self) -> int:
        with self._lock:
            return len(self._cache)
