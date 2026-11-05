"""
HMAC-SHA256 Webhook Verifier & Anti-Replay Guard
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import hmac
import hashlib
import time
import threading
from typing import Set

class HMACReplaySentinel:
    """
    Cryptographic verification with constant-time comparison and replay attack mitigation.
    """
    def __init__(self, secret: str, max_drift_seconds: float = 300.0):
        if not secret:
            raise ValueError("Secret key cannot be empty")
        self.secret = secret.encode("utf-8")
        self.max_drift = max_drift_seconds
        self._seen_nonces: Set[str] = set()
        self._lock = threading.Lock()

    def generate_signature(self, payload: str, timestamp: int, nonce: str) -> str:
        data = f"{timestamp}.{nonce}.{payload}".encode("utf-8")
        return hmac.new(self.secret, data, hashlib.sha256).hexdigest()

    def verify(self, payload: str, timestamp: int, nonce: str, signature: str) -> bool:
        now = time.time()
        if abs(now - timestamp) > self.max_drift:
            return False

        with self._lock:
            if nonce in self._seen_nonces:
                return False
            self._seen_nonces.add(nonce)

        expected = self.generate_signature(payload, timestamp, nonce)
        return hmac.compare_digest(expected, signature)
