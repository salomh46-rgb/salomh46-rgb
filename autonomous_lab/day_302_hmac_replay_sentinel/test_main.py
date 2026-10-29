import unittest
import time
from main import HMACReplaySentinel

class TestHMACSentinel(unittest.TestCase):
    def setUp(self):
        self.sentinel = HMACReplaySentinel("secret_key_123", max_drift_seconds=60.0)

    def test_valid_signature(self):
        ts = int(time.time())
        nonce = "nonce_1"
        payload = '{"amount": 50000, "currency": "UZS"}'
        sig = self.sentinel.generate_signature(payload, ts, nonce)
        self.assertTrue(self.sentinel.verify(payload, ts, nonce, sig))

    def test_replay_attack_rejected(self):
        ts = int(time.time())
        nonce = "nonce_replay"
        payload = '{"event": "payment_success"}'
        sig = self.sentinel.generate_signature(payload, ts, nonce)
        self.assertTrue(self.sentinel.verify(payload, ts, nonce, sig))
        self.assertFalse(self.sentinel.verify(payload, ts, nonce, sig))

    def test_timestamp_drift_rejected(self):
        expired_ts = int(time.time()) - 3600
        nonce = "nonce_old"
        payload = '{"event": "old"}'
        sig = self.sentinel.generate_signature(payload, expired_ts, nonce)
        self.assertFalse(self.sentinel.verify(payload, expired_ts, nonce, sig))

if __name__ == "__main__":
    unittest.main()
