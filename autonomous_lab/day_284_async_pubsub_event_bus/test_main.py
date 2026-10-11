import unittest
from main import AsyncEventBus

class TestAsyncEventBus(unittest.TestCase):
    def test_exact_topic_delivery(self):
        bus = AsyncEventBus()
        received = []
        bus.subscribe("orders.created", lambda t, p: received.append(p))
        bus.publish("orders.created", {"order_id": 99})
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["order_id"], 99)

    def test_wildcard_matching(self):
        bus = AsyncEventBus()
        events = []
        bus.subscribe("billing.*", lambda t, p: events.append(t))
        bus.publish("billing.success", 1)
        bus.publish("billing.refunded", 2)
        bus.publish("user.login", 3)
        self.assertEqual(len(events), 2)
        self.assertIn("billing.success", events)
        self.assertIn("billing.refunded", events)

if __name__ == "__main__":
    unittest.main()
