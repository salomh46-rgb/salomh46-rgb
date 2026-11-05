import unittest
import time
from main import TokenBucketRateLimiter

class TestTokenBucketRateLimiter(unittest.TestCase):
    def test_initial_capacity(self):
        limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2.0)
        self.assertAlmostEqual(limiter.available_tokens(), 10.0, delta=0.5)

    def test_acquire_success_and_failure(self):
        limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
        self.assertTrue(limiter.acquire(3))
        self.assertTrue(limiter.acquire(2))
        self.assertFalse(limiter.acquire(1))

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            TokenBucketRateLimiter(capacity=0, refill_rate=1.0)
        with self.assertRaises(ValueError):
            TokenBucketRateLimiter(capacity=5, refill_rate=-1.0)

if __name__ == "__main__":
    unittest.main()
