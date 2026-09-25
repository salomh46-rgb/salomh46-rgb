import unittest
from main import TokenBucketRateLimiter, compute_hmac_signature

class TestRateLimiter(unittest.TestCase):
    def test_acquire_tokens(self):
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
        self.assertTrue(limiter.acquire(3))
        self.assertTrue(limiter.acquire(2))
        self.assertFalse(limiter.acquire(1))

    def test_hmac_signature(self):
        sig = compute_hmac_signature("secret_key", "test_payload")
        self.assertIsInstance(sig, str)
        self.assertEqual(len(sig), 64)

if __name__ == '__main__':
    unittest.main()
