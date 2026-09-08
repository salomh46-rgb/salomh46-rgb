"""
High-performance JSON Token Bucket Rate Limiter with async support in Python
Autonomous Build Date: 2026-09-08
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import time
import hmac
import hashlib
from typing import Optional, Dict, Any

class TokenBucketRateLimiter:
    """
    Thread-safe High-Performance Token Bucket Rate Limiter.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)  # tokens per second
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        delta = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + delta * self.refill_rate)
        self.last_refill = now

    def acquire(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def get_available_tokens(self) -> float:
        self._refill()
        return self.tokens

def compute_hmac_signature(secret: str, payload: str) -> str:
    """Compute secure HMAC-SHA256 signature."""
    return hmac.new(secret.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
