import unittest
from main import PriorityTaskQueue

class TestPriorityTaskQueue(unittest.TestCase):
    def test_priority_ordering(self):
        q = PriorityTaskQueue(aging_rate=0.0)
        q.push("low", "data1", base_priority=50)
        q.push("critical", "data2", base_priority=1)
        q.push("medium", "data3", base_priority=20)

        task, _ = q.pop()
        self.assertEqual(task, "critical")
        task, _ = q.pop()
        self.assertEqual(task, "medium")
        task, _ = q.pop()
        self.assertEqual(task, "low")

    def test_empty_pop(self):
        q = PriorityTaskQueue()
        self.assertIsNone(q.pop())

if __name__ == "__main__":
    unittest.main()
