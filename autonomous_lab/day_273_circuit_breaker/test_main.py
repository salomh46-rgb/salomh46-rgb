import unittest
import time
from main import CircuitBreaker, CircuitState, CircuitBreakerOpenException

class TestCircuitBreaker(unittest.TestCase):
    def test_normal_operation(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        res = cb.call(lambda x: x * 2, 5)
        self.assertEqual(res, 10)
        self.assertEqual(cb.state, CircuitState.CLOSED)

    def test_trip_to_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
        def faulty():
            raise RuntimeError("Database timeout")

        with self.assertRaises(RuntimeError):
            cb.call(faulty)
        with self.assertRaises(RuntimeError):
            cb.call(faulty)
        self.assertEqual(cb.state, CircuitState.OPEN)

        with self.assertRaises(CircuitBreakerOpenException):
            cb.call(faulty)

    def test_half_open_recovery(self):
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        with self.assertRaises(RuntimeError):
            cb.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        self.assertEqual(cb.state, CircuitState.OPEN)
        time.sleep(0.06)
        res = cb.call(lambda: "recovered")
        self.assertEqual(res, "recovered")
        self.assertEqual(cb.state, CircuitState.CLOSED)

if __name__ == "__main__":
    unittest.main()
