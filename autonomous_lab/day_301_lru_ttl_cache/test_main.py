import unittest
import time
from main import LRUTTLCache

class TestLRUTTLCache(unittest.TestCase):
    def test_lru_eviction(self):
        cache = LRUTTLCache(capacity=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.get("a")  # access "a", makes "b" least recently used
        cache.set("c", 3)  # should evict "b"
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("c"), 3)

    def test_ttl_expiry(self):
        cache = LRUTTLCache(capacity=5, default_ttl_seconds=0.05)
        cache.set("temp", "hello")
        self.assertEqual(cache.get("temp"), "hello")
        time.sleep(0.06)
        self.assertIsNone(cache.get("temp"))

    def test_delete(self):
        cache = LRUTTLCache(capacity=5)
        cache.set("k", "v")
        self.assertTrue(cache.delete("k"))
        self.assertFalse(cache.delete("k"))

if __name__ == "__main__":
    unittest.main()
