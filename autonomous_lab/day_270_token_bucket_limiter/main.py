"""
Thread-safe Token Bucket Rate Limiter
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import time
import threading
from typing import Optional

class TokenBucketRateLimiter:
    """
    High-performance Token Bucket Rate Limiter for API rate limiting and burst management.
    """
    def __init__(self, capacity: int, refill_rate: float):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive")
            
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)  # tokens per second
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        delta = now - self.last_refill
        if delta > 0:
            self.tokens = min(self.capacity, self.tokens + (delta * self.refill_rate))
            self.last_refill = now

    def acquire(self, tokens: int = 1) -> bool:
        """Attempt to consume tokens. Returns True if granted, False otherwise."""
        if tokens <= 0:
            return True
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def available_tokens(self) -> float:
        """Returns the current number of available tokens."""
        with self._lock:
            self._refill()
            return self.tokens
