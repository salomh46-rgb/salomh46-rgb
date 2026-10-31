import unittest
from main import RetryEngine

class TestRetryEngine(unittest.TestCase):
    def test_success_first_attempt(self):
        engine = RetryEngine(max_attempts=3, base_delay=0.01)
        res = engine.execute(lambda: 42)
        self.assertEqual(res, 42)

    def test_retry_eventual_success(self):
        engine = RetryEngine(max_attempts=4, base_delay=0.01)
        tracker = {"count": 0}
        def flakey():
            tracker["count"] += 1
            if tracker["count"] < 3:
                raise ConnectionError("Network down")
            return "online"

        res = engine.execute(flakey)
        self.assertEqual(res, "online")
        self.assertEqual(tracker["count"], 3)

    def test_max_attempts_exceeded(self):
        engine = RetryEngine(max_attempts=2, base_delay=0.01)
        with self.assertRaises(ValueError):
            engine.execute(lambda: (_ for _ in ()).throw(ValueError("permanent error")))

if __name__ == "__main__":
    unittest.main()
