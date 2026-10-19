import unittest
from main import ConsistentHashRing

class TestConsistentHashRing(unittest.TestCase):
    def test_routing(self):
        ring = ConsistentHashRing(replicas=50)
        ring.add_node("cache-srv-01")
        ring.add_node("cache-srv-02")
        ring.add_node("cache-srv-03")

        node_a = ring.get_node("user_session_1001")
        node_b = ring.get_node("user_session_1002")
        self.assertIn(node_a, ["cache-srv-01", "cache-srv-02", "cache-srv-03"])
        self.assertIn(node_b, ["cache-srv-01", "cache-srv-02", "cache-srv-03"])

    def test_remove_node(self):
        ring = ConsistentHashRing(replicas=20)
        ring.add_node("srv-01")
        ring.remove_node("srv-01")
        self.assertIsNone(ring.get_node("key"))

if __name__ == "__main__":
    unittest.main()
